from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
import django.utils
import django.utils.timesince
from django.core.exceptions import SuspiciousFileOperation
import django.utils.timezone
import datetime
import os
import socialmedia.settings as settings
def rename_image(instance, filename):
    """
    Rename the uploaded image file to the username of the user.
    """
    # Get the file extension
    ext = filename.split('.')[-1]
    
    # New filename is the username with the original file extension
    new_filename = f"{instance.user.username}.{ext}"
    
    # Return the upload path
    return os.path.join('profiles/images', new_filename)
def rename_bg_image(instance, filename):
    """
    Rename the uploaded image file to the username of the user.
    """
    # Get the file extension
    ext = filename.split('.')[-1]
    
    # New filename is the username with the original file extension
    new_filename = f"{instance.user.username}.{ext}"
    
    # Return the upload path
    return os.path.join('profiles/bg/images', new_filename)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    self_introduction = models.TextField(default=" ", blank=True, null = True)
    name = models.CharField(max_length=250, default ="" )
    image = models.ImageField(upload_to=rename_image, default=settings.MEDIA_ROOT + "/images/default.png", null=True)
    bg_image = models.ImageField(upload_to=rename_bg_image, null=True)
    def __str__(self):
        return self.user.username
def save(self, *args, **kwargs):
    if self.pk:  # Check if this is an update to an existing object
        old_image = Post.objects.get(pk=self.pk).image
        if old_image and old_image != self.image:  # If the image is being updated
            try:
                old_image_path = old_image.path
                # Ensure the path is within MEDIA_ROOT
                if not old_image_path.startswith(settings.MEDIA_ROOT):
                    raise SuspiciousFileOperation(f"Path {old_image_path} is outside of MEDIA_ROOT.")
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            except SuspiciousFileOperation:
                # Handle the case where the file operation is suspicious
                pass
    super().save(*args, **kwargs)
    def image_url(self):
        """
        Return the URL of the image or a default image if none exists.
        """
        if self.image and self.image.url:
            return self.image.url
        return '/media/img/default.png'  # Path to the default image
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.name = instance.username
        user_profile.save()
post_save.connect(create_profile, sender=User)
class Post(models.Model):
    user = models.ForeignKey(User,
                             related_name="dweets",default='',
                             on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="created at", null=True)
    name = models.CharField(default="", max_length=250)
Post.created_at = datetime.datetime.now()
