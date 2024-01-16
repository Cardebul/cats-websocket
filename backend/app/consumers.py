import json
from logging import info as i

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token

from .models import ChatMessage, ChatRoom, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['user_id']
        self.flag = bool(int(self.room_name))
        self.room_group_name = f"chat_{self.room_name}"
        i(f"CONNECT {self.room_group_name}")
        try:
            self.user = await self.get_current_user(self.scope['user_token'])
        except Exception:
            self.flag = False
        if self.room_name == '0' or not self.flag:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()
        else:
            i('TWO PERSON')
            self.user_to = await self.get_user_to(int(self.scope['user_id']))
            users = sorted([self.user, self.user_to])
            self.host, self.client = users
            self.chat_room, _ = await self.get_main_room(self.host, self.client)
            self.room_name = '_'.join(map(lambda x: x.username, users))
            self.room_group_name = f'chat_{self.room_name}'
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        i(f"RECEIVE {self.user}")

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        context = {
            "type": "chat.message",
            "message": message,
            "username": self.user.username or 'username'
        }
        await self.add_chat_message(message)

        await self.channel_layer.group_send(
            self.room_group_name, context
        )

    async def chat_message(self, event):

        message = event["message"]
        username = event["username"]
        i(f'EVENT {username}')

        await self.send(text_data=json.dumps({"message": message, "username": username}))

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
        if self.flag:
            return ChatMessage.objects.create(
                chat=self.chat_room, user=self.user, message=message)
        return ChatMessage.objects.create(
            chat=None, user=self.user, message=message)
