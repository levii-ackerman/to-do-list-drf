from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from datetime import timedelta

from .models import Tag, Task

class TaskCreateSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        slug_field = 'name',
        queryset = Tag.objects.all(),
        required = False,
        allow_null = True
    )
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'tag', 'task_level', 'deadline']
        extra_kwargs = {
            'title': {'required': True},
            'tag': {'required': False},
            'task_level': {'required': True},
        }

    def validate_title(self, title):
        if not title.strip():
            raise ValidationError("must been not empty title")
        if len(title) < 3:
            raise ValidationError("Sarlavha kamida 3 ta harfdan katta bo'lishi kerak")
        return title
    
    def validate_deadline(self, deadline):
        if deadline < timezone.now():
            raise ValidationError("Deadline hozirgi vaqtdan keyin bo'lishi kerak")
        return deadline
    
    def validate(self, data):
        data = super(TaskCreateSerializer, self).validate(data)
        deadline = data.get('deadline')
        if deadline and deadline > timezone.now() + timedelta(days=365):
            raise ValidationError("Deadline muddati 1 yildan oshmasligi kerak")
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super(TaskCreateSerializer, self).create(validated_data)
    
class TaskUpdateSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Tag.objects.all(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = Task
        fields = ['title', 'description', 'tag', 'task_level', 'deadline', 'is_done']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'tag': {'required': False},
            'task_level': {'required': False},
            'deadline': {'required': False},
            'is_done': {'required': False}
        }

    def validate_title(self, title):
        if len(title) < 3 or len(title) > 30:
            raise ValidationError("title 3 ta belgidan ko'p yokida 30 dan kamroq bo'lishi kerak")
        if title.isnumeric():
            raise ValidationError("title faqat raqamlardan iborat bo'lmasligi kerak")
        if not title.split():
            raise ValidationError("title bo'sh bo'lmasligi kerak")
        return title
    
    def validate_deadline(self, deadline):
        if deadline < timezone.now():
            raise ValidationError("deadline vaqti o'tgan vaqt bo'lmasligi kerak")
        if deadline > timezone.now() + timedelta(days=365):
            raise ValidationError("deadline muddati 1 yildan ko'p bo'lmasligi kerak")
        return deadline
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance