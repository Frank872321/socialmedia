from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
import django.utils
import django.utils.timesince
import django.utils.timezone
import datetime
import os
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
    image = models.ImageField(upload_to=rename_image, default="/default.png", null=True)
    bg_image = models.ImageField(upload_to=rename_bg_image, null=True)
    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        """
        Override save to delete the old image if it exists and a new image is uploaded.
        """
        if self.pk:  # Ensure the object already exists
            try:
                old_image = Profile.objects.get(pk=self.pk).image
                if old_image and old_image != self.image:  # Check if the image is different
                    old_image_path = old_image.path
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
            except Profile.DoesNotExist:
                pass  # Handle the case where no previous instance exists
        super().save(*args, **kwargs)
    def image_url(self):
        """
        Return the URL of the image or a default image if none exists.
        """
        if self.image and self.image.url:
            return self.image.url
        return '/media/defaults/default_profile.png'  # Path to the default image
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
