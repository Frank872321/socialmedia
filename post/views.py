from django.http import HttpResponse
from django.template import loader
from .models import Post, Profile
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
# Create your views here.
def main(request):
  posts = Post.objects.all()
  user = request.user.get_username()
  template = loader.get_template('main.html ')
  if request.POST.get('content'):
    post = Post()
    post.user = request.user
    post.body = request.POST.get('content')
    post.save()
    return redirect("home")
  return HttpResponse(template.render({'posts': posts}, request))
def profiles(request, user_id):
  profile1 = User.objects.filter(username=user_id).values()[0]
  profile2 = Profile.objects.filter(user_id=profile1["id"])
  profile = profile2.values()[0]
  post = Post.objects.filter(user_id=profile1['id']).values()
  template = loader.get_template('profile.html')
  context = {
    'profile': profile,
    'post': post,
    'username': profile1["username"],
    'self_introduction': profile["self_introduction"],
  }
  return HttpResponse(template.render(context, request))