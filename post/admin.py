from django.contrib import admin

# Register your models here.
from .models import Profile, Post
from django.contrib.auth.models import User, Group

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline]

admin.site.register(Post)
admin.site.register(Profile)