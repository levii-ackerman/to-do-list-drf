from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Friend, FriendShip

@receiver(post_save, sender=Friend)
def create_friendship_on_accept(sender, instance, created, **kwargs):
    if not created and instance.friend_status == "accepted":
        user_1 = instance.from_user
        user_2 = instance.to_user

        if not FriendShip.objects.filter(user_1=user_1, user_2=user_2).exists() and not FriendShip.objects.filter(user_1=user_2, user_2=user_1).exists():
            FriendShip.objects.create(user_1=user_1, user_2=user_2)