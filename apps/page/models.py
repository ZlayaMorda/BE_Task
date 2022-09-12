from django.db import models

from apps import user


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='pages')

    owner = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('user.CustomUser', related_name='follows')

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('user.CustomUser', related_name='requests')

    unblock_date = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)

    reply_to = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, related_name='replies')

    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='reactions')

    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
