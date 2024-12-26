from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room, Message, BadWords
from .forms import PrivateGroupForm
import re
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

@login_required
def rooms(request):
    rooms = Room.objects.filter(is_private=False)
    invited_rooms = Room.objects.filter(members__username__icontains=request.user.username)
    return render(request, 'room/rooms.html', {'rooms': rooms, 'invited': invited_rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]
    banned_words = list(BadWords.objects.all().values_list('name'))
    rooms = Room.objects.filter(is_private=False)
    invited_rooms = Room.objects.filter(members__username__icontains=request.user.username)
    flag = "false"
    user = request.user.get_username()
    if request.method == "POST":
        content = request.POST.get("content")
        token = content.split()
        # Detect matches
        for i in token:
            if i in banned_words:
                print("Flagged words detected:", i)
                flag = "true"
                redirect('home')


    return render(request, 'room/room.html', {'room': room, 'messages': messages, 'flagged': flag, 'word': banned_words, 'rooms': rooms, 'invited': invited_rooms,'room_slug': slug, })
def create_private_group(request):
    if request.method == 'POST':
        form = PrivateGroupForm(request.POST, user=request.user)
        if form.is_valid():
            group = form.save(commit=False)
            group.is_private=True
            group.save()
            # Add the current user as a member automatically
            group.members.add(request.user)
            return redirect('rooms')  # Adjust this to the desired redirect
    else:
        form = PrivateGroupForm(request.POST, user=request.user)

    return render(request, 'room/create_room.html', {'form': form})
def fetch_link_preview(request):
    url = request.GET.get('url')
    if not url:
        return JsonResponse({'error': 'No URL provided'}, status=400)
    
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get OpenGraph metadata
        og_image = soup.find('meta', property='og:image')
        og_title = soup.find('meta', property='og:title')
        og_description = soup.find('meta', property='og:description')
        
        data = {
            'title': og_title['content'] if og_title else '',
            'description': og_description['content'] if og_description else '',
            'image': og_image['content'] if og_image else ''
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)