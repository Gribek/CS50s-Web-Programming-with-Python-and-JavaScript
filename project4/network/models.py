from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)


class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='followers')

    class Meta:
        unique_together = ['follower', 'following']
