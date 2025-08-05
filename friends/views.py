from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Friend, FriendShip
from .serializers import FriendRequestSerializer, FriendResponseSerializer, FriendShipSerializer

class FriendRequestView(CreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated, ]

class FriendRequestListView(ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friend.objects.filter(to_user = self.request.user, friend_status = "pending")
    
class FriendResponseView(UpdateAPIView):
    serializer_class = FriendResponseSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return get_object_or_404(Friend, id = self.kwargs['id'], to_user = self.request.user)
    

class FriendListView(ListAPIView):
    serializer_class = FriendShipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendShip.objects.filter(user_1=user) | FriendShip.objects.filter(user_2 = user)