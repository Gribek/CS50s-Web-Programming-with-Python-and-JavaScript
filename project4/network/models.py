from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_users_liking(self):
        return [like.user.id for like in self.who_likes.all()]


class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='followers')

    class Meta:
        unique_together = ['follower', 'following']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='liking')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='who_likes')

    class Meta:
        unique_together = ['user', 'post']
