from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm 
# Create your views here.
from django.dispatch import receiver
from django.contrib.auth.models import User
from post.models import Profile
from django.db.models.signals import post_save
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from post.views import main
from .forms import ProfileForm
class Login(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy(main) 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically logs the user in after registration
            return redirect('login')  # Replace 'home' with your desired landing page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def update_profile(request):
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('home')  # Replace 'profile' with the name of your profile page URL

    return render(request, 'edit.html', {
        'profile_form': profile_form
    })

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()