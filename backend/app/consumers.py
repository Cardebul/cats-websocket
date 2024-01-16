# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from logging import info as i
from rest_framework.authtoken.models import Token
from .models import User, ChatRoom, ChatMessage
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['user_id']
        self.flag = bool(int(self.room_name))
        self.room_group_name = f"chat_{self.room_name}"
        i("CONNECT")
        i(self.room_name)
        self.user = await self.get_current_user(self.scope['user_token'])
        if self.room_name == '0':
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()
        else:
            i('ELSE BLOCK')
            self.user_to = await self.get_user_to(int(self.scope['user_id']))
            users = sorted([self.user, self.user_to])
            self.host, self.client = users
            self.chat_room, _ = await self.get_main_room(self.host, self.client)
            self.room_name = '_'.join(map(lambda x: x.username, users))
            self.room_group_name = f'chat_{self.room_name}'
            i(self.user)
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()
             

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        i("Receive")
        
        i(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        context = {
            "type": "chat.message",
            "message": message,
            "username": self.user.username or 'username'
            }
        i(await self.add_chat_message(message))

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, context
        )

    # Receive message from room group
    async def chat_message(self, event):
        i('EVENT')
        i(datetime.now())
        
        i(event)
        message = event["message"]
        username = event["username"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username}))
    
    
    # @database_sync_to_async
    # def create_message(self, message):
    #     return Message.objects.create(text=message)
    
    @database_sync_to_async
    def get_current_user(self, token):
        return Token.objects.select_related('user').get(key=token).user
    
    @database_sync_to_async
    def get_user_to(self, id):
        return User.objects.get(pk=id)
    
    @database_sync_to_async
    def get_main_room(self, host, client):
        return ChatRoom.objects.get_or_create(user=host, user_to=client)
    
    @database_sync_to_async
    def add_chat_message(self, message):
        i('addchatMESS')
        if self.flag:
            return ChatMessage.objects.create(chat=self.chat_room, user=self.user, message=message)
        return ChatMessage.objects.create(chat=None, user=self.user, message=message)
        
        
        
        