from random import choice

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import Markdown

from . import util
from encyclopedia.forms import AddEntryForm, EditEntryForm


def index(request):
    """List all wiki entries."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry_title):
    """Display single wiki entry."""
    entry = util.get_entry(entry_title)
    if entry is None:
        raise Http404
    mark_downer = Markdown()
    ctx = {'content': mark_downer.convert(entry), 'title': entry_title}
    return render(request, 'encyclopedia/entry_page.html', context=ctx)


def search(request):
    """Find entry in encyclopedia."""
    query = request.GET.get('query')
    entries = util.list_entries()
    if query in entries:
        return entry_page(request, entry_title=query)
    else:
        ctx = {'query': query,
               'entries': [e for e in entries if query.lower() in e.lower()]}
        return render(request, 'encyclopedia/search.html', context=ctx)


def random_page(request):
    """Display random wiki entry."""
    random_entry = choice(util.list_entries())
    return entry_page(request, random_entry)


def new_entry(request):
    """Add new entry to the wiki"""
    if request.method == 'POST':
        form = AddEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            util.save_entry(title, form.cleaned_data['content'])
            return redirect(
                reverse('entry_page', kwargs={'entry_title': title}))
    else:
        form = AddEntryForm()

    return render(request, 'encyclopedia/new_entry.html', {'form': form})


def edit_entry(request, entry_title):
    """Edit selected entry."""
    if request.method == 'POST':
        form = EditEntryForm(request.POST)
        if form.is_valid():
            util.save_entry(entry_title, form.cleaned_data['content'])
            return redirect(
                reverse('entry_page', kwargs={'entry_title': entry_title}))
    else:
        form = EditEntryForm()
        form.initial['content'] = util.get_entry(entry_title)

    return render(request, 'encyclopedia/edit_entry.html',
                  {'form': form, 'title': entry_title})
