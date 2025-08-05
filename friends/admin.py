from django.contrib import admin
from .models import Friend, FriendShip

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'friend_status']

@admin.register(FriendShip)
class FriendShipAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_1', 'user_2', 'created_at']