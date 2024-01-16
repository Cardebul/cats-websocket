from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Achievement, AchievementCat, Cat, ChatMessage, ChatRoom,
                     User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = ("email", "username")


@admin.register(ChatRoom)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatMessage)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Cat)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Achievement)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(AchievementCat)
class IngredientAdmin(admin.ModelAdmin):
    pass
