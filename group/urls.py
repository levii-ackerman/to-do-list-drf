from django.urls import path
from .views import (
    GroupCreateView, GroupUpdateView, GroupDeleteView, 
    GroupAddMemberView, GroupMemberList, GroupMemberDeleteView, 
    GroupTaskCreateView, GroupTaskListView, GroupTaskUpdateView, 
    GroupTaskDeleteView,  GroupSubTaskCreateView, GroupSubTaskUpdateView,
    GroupSubTaskDeleteView, GroupSubTaskListView, SubTaskToggleDoneView
)
urlpatterns = [
    path('create/', GroupCreateView.as_view(), name='group-create'),
    path('<uuid:id>/update/', GroupUpdateView.as_view(), name='group-update'),
    path('<uuid:id>/delete/', GroupDeleteView.as_view(), name='group-delete'),
    path('add-member/', GroupAddMemberView.as_view(), name='add-member'),
    path('<uuid:group_id>/members/', GroupMemberList.as_view(), name='members-list'),
    path('<uuid:group_id>/member/<uuid:user_id>/delete/', GroupMemberDeleteView.as_view(), name='member-delete'),
    path('<uuid:group_id>/create-task/', GroupTaskCreateView.as_view(), name='create-task-gr'),
    path('<uuid:id>/gr-task-update/', GroupTaskUpdateView.as_view(), name='group-task-update'),
    path('<uuid:id>/gr-task-delete/', GroupTaskDeleteView.as_view(), name='gr-task-delete'),
    path('<uuid:group_id>/task-list/', GroupTaskListView.as_view(), name='group-task-list'),
    path('subtask-create/', GroupSubTaskCreateView.as_view(), name='subtask-create'),
    path('<uuid:id>/subtask-update/', GroupSubTaskUpdateView.as_view(), name='subtask-update'),
    path('<uuid:id>/subtask-delete/', GroupSubTaskDeleteView.as_view(), name='subtask-delete'),
    path('<uuid:group_id>/subtask-list/', GroupSubTaskListView.as_view(), name='subtask-list'),
    path('<uuid:id>/subtask-done/', SubTaskToggleDoneView.as_view(), name='subtask-done')
]