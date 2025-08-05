from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Task, Tag
from .serializers import TaskCreateSerializer, TaskUpdateSerializer

class TasksListView(ListAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.all()

class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        data = {
            'success': True,
            'message': "task successfully created",
            'code': 200
        }
        return Response(data, status=200)
    
class TaskUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        task = get_object_or_404(Task, id=pk, user=request.user)
        serializer = TaskUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.deadline = data.get('deadline', task.deadline)
            task.is_done = data.get('is_done', task.is_done)
            task.task_level = data.get('task_level', task.task_level)
            task.tag = data.get('tag', task.tag)
            task.save()
            return Response(
                {
                    'success': True,
                    'message': 'Task successfully updated',
                },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    
class TaskDeleteVIew(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        task = get_object_or_404(Task, id=pk, user=request.user)
        task.delete()
        return Response(
            {
                'success': True,
                'message': 'task successfully deleted'
            },
            status=status.HTTP_200_OK
        )