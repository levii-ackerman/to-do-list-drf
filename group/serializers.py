from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Group, GroupMember, GroupSubTask, GroupTask
from shared.validators import validate_deadline, validate_title
from datetime import timedelta

User = get_user_model()

class GroupCreateSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'owner', 'description']
        read_only_fields = ['id', 'owner']

    def validate_name(self, value):
        user = self.context['request'].user
        if Group.objects.filter(name=value, owner=user).exists():
            raise ValidationError(
                {
                    'success': False,
                    'message': "Bunday nom bilan guruh yaratgansiz"
                }
            )
        return value
        
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    
class GroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'description']
    
    def validate_name(self, value):
        if not value:
            raise ValidationError(
                {
                    'success': False,
                    'message': "name bo'lishi kerak"
                }
            )
        return value
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class GroupAddMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    group_name = serializers.CharField(source='group_id.name', read_only=True)
    class Meta:
        model = GroupMember
        fields = ['id', 'user_id', 'group_id', 'username', 'group_name']
        read_only_fields = ['id']

    def validate(self, data):
        group = data.get('group_id')
        user = data.get('user_id')

        if GroupMember.objects.filter(user_id = user, group_id = group).exists():
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Bu foydalanuvchi allaqachon guruhda mavjud'
                }
            )
        return data
    
    def validate_user_id(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Bunday foydalanuvchi mavjud emas'
                }
            )
        return value
    
    def validate_group_id(self, value):
        if not Group.objects.filter(id=value.id).exists():
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Bunday guruh mavjud emas'
                }
            )
        return value
    
class GroupTaskCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(validators=[validate_title])
    deadline = serializers.DateTimeField(validators=[validate_deadline], required=False)
    
    class Meta:
        model = GroupTask
        fields = ['id', 'title', 'description', 'deadline', 'is_done']

    def validate(self, attrs):
        user = self.context['request'].user
        group_id = self.context.get('group_id')

        group = Group.objects.filter(id=group_id, owner = user).first()
        if group is None:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Bunday guruh mavjud emas"
                }
            )
        
        is_member = GroupMember.objects.filter(group_id=group_id, user_id = user).exists()
        if not is_member:
            raise ValidationError(
                {
                    'success': False,
                    'messaeg': 'Siz bu guruhda mavjud emassiz'
                }
            )
        return attrs

    
class GroupTaskUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_title])
    deadline = serializers.DateTimeField(validators=[validate_deadline])

    class Meta:
        model = GroupTask
        fields = ['title', 'description', 'is_done', 'deadline']

    def update(self, instance, validated_data):
        for attrs, value in validated_data.items():
            setattr(instance, attrs, value)
        instance.save()
        return instance

class GroupSubTaskCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    member = serializers.SerializerMethodField()
    title = serializers.CharField(validators=[validate_title])
    deadline = serializers.DateTimeField(validators=[validate_deadline], required=False)

    class Meta:
        model = GroupSubTask
        fields = ['id', 'title', 'description', 'is_done', 'deadline', 'gr_task', 'member_id', 'member']


    def get_member(self, obj):
        return {
            'username': obj.member_id.user_id.username,
            'group_name': obj.member_id.group_id.name
        }

    def validate(self, attrs):
        user = self.context['request'].user
        member = attrs.get('member_id')

        if not member:
            raise ValidationError(
                {
                    'success': False,
                    'message': "member_id: A'zoni ko'rsatish kerak"
                }
            )
        
        if member.user_id != user:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Siz faqat o'zingiz uchun topshiriq qo'sha olasiz"
                }
            )
        return attrs
    
class GroupSubTaskUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_title])
    deadline = serializers.DateTimeField(validators=[validate_deadline], required=False)

    class Meta:
        model = GroupSubTask
        fields = ['title', 'description', 'deadline', 'is_done']

    def update(self, instance, validated_data):
        for attrs, value in validated_data.items():
            setattr(instance, attrs, value)
        instance.save()
        return instance
