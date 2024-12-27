from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Post, Profile
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render, get_object_or_404
import markdown
import markdown2
from django.utils.html import mark_safe

def toggle_dark_mode(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.dark_mode = not profile.dark_mode  # Toggle value
        profile.save()
        return JsonResponse({"dark_mode": profile.dark_mode})
    return JsonResponse({"error": "Invalid request"}, status=400)
# Create your views here.
def main(request):
  posts = Post.objects.all().order_by('-created_at')
  for post in posts:
        post.body_html = markdown.markdown(post.body, extensions=['extra', 'codehilite'])
  template = loader.get_template('main.html ')
  link = "https://lqdoj.edu.vn"
  if request.POST.get('content'):
    post = Post()
    post.user = request.user
    post.body = request.POST.get('content')
    profile1 = User.objects.filter(username=request.user).values()[0]
    profile2 = Profile.objects.filter(user_id=profile1["id"])
    profile = profile2.values()[0]
    post.name = profile["name"]
    post.save()
    return redirect("home")
  post = Post()
  return HttpResponse(template.render({'posts': posts, 'link':link}, request))
def profiles(request, user_id):
    profile_user = get_object_or_404(User, username=user_id)
    profile = profile_user.profile
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')

    # Convert self-introduction to Markdown
    profile.self_introduction_html = mark_safe(markdown2.markdown(profile.self_introduction or ""))

    # Convert each post body to Markdown
    for post in posts:
        post.body_html = mark_safe(markdown2.markdown(post.body or "", extras=["fenced-code-blocks", "tables"]))

    context = {
        'profile': profile,
        'posts': posts,
        'username': user_id,
        'name': profile_user.get_full_name(),
    }
    return render(request, 'profile.html', context)