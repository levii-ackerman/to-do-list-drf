from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import (GroupCreateSerializer, GroupUpdateSerializer, GroupAddMemberSerializer, 
                          GroupTaskCreateSerializer, GroupSubTaskCreateSerializer, GroupTaskUpdateSerializer,
                          GroupSubTaskUpdateSerializer
)
from .models import Group, GroupMember, GroupTask, GroupSubTask

User = get_user_model()

class GroupCreateView(CreateAPIView):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GroupCreateSerializer

class GroupUpdateView(UpdateAPIView):
    serializer_class = GroupUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'

    def get_queryset(self):
        return Group.objects.filter(owner=self.request.user)
           
class GroupDeleteView(DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'

    def get_queryset(self):
        return Group.objects.filter(owner=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response(
            {
                'success': True,
                'message': 'Group uchirildi'
            },
            status=status.HTTP_200_OK
        )

class GroupAddMemberView(CreateAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupAddMemberSerializer
    permission_classes = [IsAuthenticated, ]

class GroupMemberList(ListAPIView):
    serializer_class = GroupAddMemberSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        return GroupMember.objects.filter(group_id=group_id)
    
class GroupMemberDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        group_id = self.kwargs.get('group_id')
        user_id = self.kwargs.get('user_id')

        group = get_object_or_404(Group, id=group_id)
        user = get_object_or_404(User, id=user_id)

        return get_object_or_404(GroupMember, group_id=group, user_id=user)

    def delete(self, request, group_id, user_id):
        member = self.get_object()
        member.delete()
        return Response(
            {
                'success': True,
                'message': 'Member o‘chirildi'
            }
        )
    
class GroupTaskCreateView(CreateAPIView):
    serializer_class = GroupTaskCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['group_id'] = self.kwargs.get('group_id')
        return context
    
    def perform_create(self, serializer):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        serializer.save(group_id=group)

class GroupTaskUpdateView(UpdateAPIView):
    queryset = GroupTask.objects.all()
    serializer_class = GroupTaskUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'

class GroupTaskDeleteView(DestroyAPIView):
    queryset = GroupTask.objects.all()
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if instance.group_id.owner != user:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Sizda taskni o'chirish uchun ruxsat yo'q"
                }
            )
        instance.delete()
        return Response(
            {
                'success': True,
                'messaeg': "Task muvaffaqiyatli o'chirildi"
            },
            status=status.HTTP_200_OK
        )
class GroupTaskListView(ListAPIView):
    queryset = GroupTask.objects.all()
    serializer_class = GroupTaskCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        group_id = self.kwargs.get('group_id')
        return GroupTask.objects.filter(group_id = group_id)

class GroupSubTaskCreateView(CreateAPIView):
    queryset = GroupSubTask.objects.all()
    serializer_class = GroupSubTaskCreateSerializer
    permission_classes = [IsAuthenticated, ]
    
class GroupSubTaskUpdateView(UpdateAPIView):
    queryset = GroupSubTask.objects.all()
    serializer_class = GroupSubTaskUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'

class GroupSubTaskListView(ListAPIView):
    serializer_class = GroupSubTaskCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        try:
            group = Group.objects.filter(id=group_id)
        except Group.DoesNotExist:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Bunday guruh mavjud emas"
                }
            )
        return GroupSubTask.objects.filter(gr_task__group_id=group_id)

class GroupSubTaskDeleteView(DestroyAPIView):
    queryset = GroupSubTask.objects.all()
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if instance.gr_task.group_id.owner != user:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Sizda taskni o'chirish uchun ruxsat yo'q"
                }
            )
        instance.delete()
        return Response(
            {
                'success': True,
                'message': "Task muvaffaqiyatli o'chirildi"
            },
            status=status.HTTP_200_OK
        )
    
class SubTaskToggleDoneView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, id):
        user = self.request.user
        try:
            subtask = GroupSubTask.objects.select_related('member_id__user_id', 'gr_task__group_id').get(pk=id)
        except GroupSubTask.DoesNotExist:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Bunday subtask topilmadi"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if subtask.member_id.user_id != user or subtask.gr_task.group_id.owner != user:
            return Response(
                {
                    'success': False,
                    'message': "Sizda bu subtaskni holatini o'zgartirish uchun ruxsat yo'q"
                }
            )
        
        is_done = request.data.get('is_done')
        if not isinstance(is_done, bool):
            raise ValidationError(
                {
                    'success': False,
                    'message': "is_done True yoki False bo'lishi mumkin xolos"
                }
            )
        subtask.is_done = is_done
        subtask.save()

        return Response(
            {
                'success': True,
                'message': f"Subtask {'bajarilid' if is_done else 'bajarilmadi'} deb belgilandi",
                'subtask_id': subtask.id,
                'is_done': subtask.is_done
            }, status=status.HTTP_200_OK
        )