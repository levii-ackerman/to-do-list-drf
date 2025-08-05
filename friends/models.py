from django.db import models
from django.contrib.auth import get_user_model
from shared.models import BaseModel

User = get_user_model()

PENDING, REJECTED, ACCEPTED = "pending", "rejected", "accepted"

class Friend(BaseModel, models.Model):
    FRIEND_STATUS = (
        (PENDING, PENDING),
        (REJECTED, REJECTED),
        (ACCEPTED, ACCEPTED)
    )
    friend_status = models.CharField(max_length=10, choices=FRIEND_STATUS, default=PENDING)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.friend_status})"
    
class FriendShip(BaseModel, models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_as_user1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_as_user2')

    class Meta:
        unique_together = ('user_1', 'user_2')

    def __str__(self):
        return f"{self.user_1} -> {self.user_2}"