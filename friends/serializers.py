from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Friend, FriendShip

User = get_user_model()

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['id', 'from_user', 'to_user', 'friend_status']
        read_only_fields = ['from_user']

    def validate(self, data):
        user = self.context['request'].user
        to_user = data.get('to_user')

        if user ==  to_user:
            raise ValidationError(
                {
                    'success': False,
                    'message': "O'zingizga do‘stlik so‘rovi yuborolmaysiz."
                }
            )
        if Friend.objects.filter(from_user = user, to_user = to_user, friend_status = "pending").exists():
            raise ValidationError(
                {
                    'success': False,
                    'message': "Siz allaqachon bu foydalanuvchiga so‘rov yuborgansiz."
                }
            )
        if Friend.objects.filter(from_user = user, to_user = to_user, friend_status = "accepted").exists():
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Request accepted bolgan'
                }
            )
        if Friend.objects.filter(from_user = user, to_user = to_user, friend_status = "rejected").exists():
            raise ValidationError(
                {
                    'success': False,
                    'message': 'siz bloklangansiz'
                }
            )
        return data
    
    def create(self, validated_data):
        validated_data['from_user'] = self.context['request'].user
        return super().create(validated_data)
    
class FriendResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['friend_status']

    def validate_status(self, value):
        if value is not ["accepted", "rejected"]:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Faqat 'accepted' yoki 'rejected' holat bo'lishi mumkin."
                }
            )
        return value
    
class FriendShipSerializer(serializers.ModelSerializer):
    user_1 = serializers.StringRelatedField()
    user_2 = serializers.StringRelatedField()

    class Meta:
        model = FriendShip
        fields = ['id', 'user_1', 'user_2']
