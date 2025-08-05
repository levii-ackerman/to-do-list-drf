from django.urls import path
from .views import TasksListView, TaskCreateView, TaskUpdateView, TaskDeleteVIew

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('list/', TasksListView.as_view(), name='task-list'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteVIew.as_view(), name='task-delete'),
]