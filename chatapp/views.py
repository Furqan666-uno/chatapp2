from django.shortcuts import render
from .models import ChatRoom, ChatMessage
import json
from django.http import JsonResponse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'chatapp/signup.html', {'form': form})


@login_required(login_url='login')
def index(request):
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        if room_name:
            slug = slugify(room_name)
            chatroom, created = ChatRoom.objects.get_or_create(slug=slug, defaults={'name': room_name, 'created_by': request.user})
            return redirect('chatroom', slug=chatroom.slug)

    chatrooms = ChatRoom.objects.all()
    return render(request, 'chatapp/index.html', {'chatrooms': chatrooms, 'on_index': True})


@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            slug = slugify(room_name)
            if not ChatRoom.objects.filter(slug=slug).exists(): # if chat room doesnt exists, create new one 
                ChatRoom.objects.create(name=room_name, slug=slug, created_by=request.user)
                return redirect('chatroom', slug=slug)
    return redirect('index')


@login_required
def delete_room(request, slug):
    chatroom = get_object_or_404(ChatRoom, slug=slug)

    # Only allow the user who created the room to delete it
    if request.user == chatroom.created_by:
        chatroom.delete()
    return redirect('index')


def chatroom(request, slug):
    chatroom= ChatRoom.objects.get(slug=slug)
    room_slug_json= json.dumps(chatroom.slug)

    username= request.user.username  # from logged-in user
    username_json= json.dumps(username)

    messages= ChatMessage.objects.filter(room=chatroom)[0:30] # bcz room name will be chatroom name, 0 to 30 message will be shown at a time 

    return render(request, 'chatapp/room.html', {
        'chatroom': chatroom,
        'room_slug_json': room_slug_json,
        'username': username_json,
        'messages': messages,
    })

@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id, user=request.user)
    message.delete()
    return JsonResponse({'status': 'success'})
    
    
    # user= ChatRoom.objects.get(name=name)
    # username= json.dumps(username.name)
    # return render(request, 'chatapp/room.html', {'chatroom':chatroom, 'room_slug_json': room_slug_json, 'user':user, 'username':username})