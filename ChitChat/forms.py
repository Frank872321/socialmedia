from django import forms
from django.contrib.auth.models import User
from .models import Room

class PrivateGroupForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'members', 'slug']
        widgets = {
            'members': forms.CheckboxSelectMultiple,  # Allows users to select members
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass the current user to the form
        super().__init__(*args, **kwargs)
        if user:
            # Exclude the current user from the "members" selection
            self.fields['members'].queryset = User.objects.exclude(id=user.id)