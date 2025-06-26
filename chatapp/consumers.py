from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import ChatRoom, ChatMessage
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name= self.scope['url_route']['kwargs']['room_name']
        # above line will extract room_name from address path
        self.room_group_name= f'chat_{self.room_name}'

        await self.channel_layer.group_add( # activating the channel layer
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard( # closing the channel layer
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data= json.loads(text_data)
        message= data['message']
        username= data['username']
        room= data['room']

        await self.channel_layer.group_send( # sending message data to channel layer
            self.room_group_name, {'type':'chat_message', 'message':message, 'username':username, 'room':room}
        )

        await self.save_message(username, room, message) # taken from last func of consumers.py
    
    # to send message back to the client 
    async def chat_message(self, event):
        message= event['message']
        username= event['username']
        room= event['room']

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
        }))

    @sync_to_async
    def save_message(self, username, room, message): # to save messga ein the model 
        user= User.objects.get(username=username)
        room= ChatRoom.objects.get(slug=room)

        ChatMessage.objects.create(user=user, room=room, message_content=message)