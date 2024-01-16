from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Achievement, Cat, ChatMessage, ChatRoom, User
from .serializers import (AchievementSerializer, CatSerializer,
                          GetChatSerializer, UserGetSerializer)


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None


class GetUser(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class GetChat(ListAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = GetChatSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        room_id = self.kwargs['pk']
        if not room_id:
            return ChatMessage.objects.filter(chat=None)
        user, user_to = sorted([room_id, self.request.user.id])
        room, _ = ChatRoom.objects.get_or_create(
            user_id=user, user_to_id=user_to)
        return ChatMessage.objects.filter(chat=room)


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name,
                                              })
