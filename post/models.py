from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import django.utils
import django.utils.timesince
import django.utils.timezone
import datetime
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    self_introduction = models.TextField(default=" ")
    def __str__(self):
        return self.user.username
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
class Post(models.Model):
    user = models.ForeignKey(User,
                             related_name="dweets",default='',
                             on_delete=models.DO_NOTHING)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="created at", null=True)
Post.created_at = datetime.datetime.now()