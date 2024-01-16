from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Achievement, Cat, User, ChatMessage, ChatRoom
from .serializers import AchievementSerializer, CatSerializer, UserGetSerializer, GetChatSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from logging import info as i

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
        i(f'{type(room_id)}  {room_id}  GET QUERYSET USERS ')
        if not room_id:
            w = ChatMessage.objects.filter(chat=None)
            i(f'not room   {w}   ')
            return w
        user, user_to = sorted([room_id,self.request.user.id])
        room, _ = ChatRoom.objects.get_or_create(user_id=user, user_to_id=user_to)
        w = ChatMessage.objects.filter(chat=room)
        i(f'room  {room} {w}')
        return w
    def get_object(self):
        i('OBJ')
        return ChatMessage.objects.all()
    

from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    from rest_framework.authtoken.models import Token
    # print(Token.objects.all())
    return render(request, "chat/room.html", {"room_name": room_name,
                                              })
    
    
def room_api(request, pk):
    print(22)
    return Response({'status': 'good'})