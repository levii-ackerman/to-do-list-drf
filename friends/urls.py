from django.urls import path
from .views import FriendRequestView, FriendResponseView, FriendRequestListView, FriendListView

urlpatterns = [
    path('request/', FriendRequestView.as_view(), name='friend-request'),
    path('request-lists/', FriendRequestListView.as_view(), name='friend-request-list'),
    path('<uuid:id>/response/', FriendResponseView.as_view(), name='friend-response'),
]