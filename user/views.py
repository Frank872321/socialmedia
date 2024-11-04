from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from post.views import main
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