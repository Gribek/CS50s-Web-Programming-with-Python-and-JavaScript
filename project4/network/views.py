import json

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import User, Post, Following, Like
from .forms import PostForm


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("all_posts"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def all_posts(request):
    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('all_posts')
        else:
            return render(request, 'network/all_posts.html',
                          {'form': form, 'page_object': page_object})
    else:
        form = PostForm()
        return render(request, 'network/all_posts.html',
                      {'form': form, 'page_object': page_object})


def following(request):
    following_users = [u.following for u in request.user.following.all()]
    posts = Post.objects.filter(user__in=following_users).order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'network/following.html',
                  {'page_object': page_object})


def profile(request, user_id):
    current_user = request.user
    profile_user = get_object_or_404(User, pk=user_id)
    ctx = {
        'profile_user': profile_user,
        'posts': profile_user.post_set.order_by('-date'),
        'my_profile': profile_user == current_user,
        'following': Following.objects.filter(
            follower=current_user, following=profile_user).exists()
    }
    return render(request, 'network/user_profile.html', context=ctx)


def follow(request, user_id):
    try:
        Following.objects.create(follower=request.user,
                                 following=get_object_or_404(User, pk=user_id))
    except IntegrityError:
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def unfollow(request, user_id):
    obj = Following.objects.filter(follower=request.user, following=user_id)
    if obj.exists():
        obj.delete()
    return HttpResponse(status=200)


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.id != post.user.id:
        return HttpResponse(status=403)

    data = json.load(request)
    if data == post.text:
        return HttpResponse(status=200)

    post.text = data
    post.save()
    return HttpResponse(status=200)


def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    current_user = request.user
    if post.user == current_user:
        return HttpResponse(status=404)
    try:
        Like.objects.create(user=current_user, post=post)
    except IntegrityError:
        return HttpResponse(status=404)
    post.likes += 1
    post.save()
    return HttpResponse(status=200)


def unlike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    obj = Like.objects.filter(user=request.user, post=post)
    if obj.exists():
        obj.delete()
        post.likes -= 1
        post.save()
    return HttpResponse(status=200)
