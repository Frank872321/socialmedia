from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Post
from django.contrib.auth.models import User, Group

class ProfileInline(admin.StackedInline):
    model = Profile

class CustomUserAdmin(DefaultUserAdmin):
    """
    Custom admin for the User model, keeping all default functionality 
    and adding a mechanism to flag accounts created via the admin interface.
    """
    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new user creation
            obj._created_via_admin = True  # Add a custom attribute for signaling
        super().save_model(request, obj, form, change)

# Unregister the default UserAdmin and register the customized UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(Post)
admin.site.register(Profile)
