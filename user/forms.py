from django import forms
from django.contrib.auth.models import User
from post.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','self_introduction', 'image', 'bg_image']
