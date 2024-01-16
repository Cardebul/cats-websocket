from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id
    
    def __ne__(self, __value: object) -> bool:
        return self.id == __value.id
    
    def __lt__(self, __value: object) -> bool:
        return self.id < __value.id
    
    def __gt__(self, __value: object) -> bool:
        return self.id > __value.id
    
    def __le__(self, __value: object) -> bool:
        return self.id <= __value.id
    
    def __ge__(self, __value: object) -> bool:
        return self.id >= __value.id
    
    def __str__(self) -> str:
         return self.username
     
    def __repr__(self) -> str:
         return self.username
     
    class Meta:
        db_table = 'user'

class ChatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_to')
    
    class Meta:
        db_table = 'chat_room'


class ChatMessage(models.Model):
    chat = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='messages')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp', 'id')
        db_table = 'chat_message'
        
    
    def __str__(self):
        return self.message

class Achievement(models.Model):
    name = models.CharField(max_length=64)
    
    class Meta:
        db_table = 'achievement'
        

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats',
        on_delete=models.CASCADE
    )
    achievements = models.ManyToManyField(Achievement,
                                          through='AchievementCat')
    image = models.ImageField(
        upload_to='cats/images/',
        null=True,
        default=None
    )
    class Meta:
        db_table = 'cat'
        

    def __str__(self):
        return self.name


class AchievementCat(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.achievement} {self.cat}'
    
    class Meta:
        db_table = 'cat_achievement'
        


