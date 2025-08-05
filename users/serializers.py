from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, VIA_EMAIL, VIA_PHONE, NEW, VERIFIED, DONE
from shared.utility import check_user_input, send_email, check_user_type

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_or_phone'] = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'auth_status', 'auth_type']
        extra_kwargs = {
            'auth_status': {'read_only': True, 'required': False},
            'auth_type': {'read_only': True, 'required': False}
        }

    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    def auth_validate(self, data):
        user_input = str(data.get('email_or_phone')).lower()
        print(user_input)
        user_type = check_user_input(user_input)

        if user_type == "via_email":
            data = {
                'auth_type': VIA_EMAIL,
                'email': user_input
            }
        elif user_type == "via_phone":
            data = {
                'auth_type': VIA_PHONE,
                'phone': user_input
            }
        return data
    
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)

        if user.auth_type == VIA_EMAIL:
            code = user.create_code(verify_type=VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_code(verify_type=VIA_PHONE)
            send_email(user.email, code)
        else:
            data = {
                'success': False,
                'message': 'Createda xatolik'
            }
            raise ValidationError(data)
        user.save()
        return user
    
    def validate_email_or_phone(self, value):
        value = value.lower()
        if value and User.objects.filter(email=value).exists():
            data = {
                'success': False,
                'message': 'This is email already exists'
            }
            raise ValidationError(data)
        elif value and User.objects.filter(phone=value).exists():
            data = {
                'success': False,
                'message': 'This is phone already exists'
            }
            raise ValidationError(data)
        return value
    
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data
    
class ChangeUserInformationSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            data = {
                'success': False,
                'message': 'both password must been bir xil'
            }
            raise ValidationError
        validate_password(password)
        validate_password(confirm_password)

        return data
    @staticmethod
    def validate_first_name(first_name):
        if len(first_name) < 3 or len(first_name) > 25:
            data = {
                'success': False,
                'message': 'first_name must been between 3 and 25'
            }
            raise ValidationError(data)
        return first_name
    @staticmethod
    def validate_first_name(last_name):
        if len(last_name) < 3 or len(last_name) > 25:
            data = {
                'success': False,
                'message': 'first_name must been between 3 and 25'
            }
            raise ValidationError(data)
        return last_name
    
    @staticmethod
    def validate_first_name(username):
        if len(username) < 3 or len(username) > 25:
            data = {
                'success': False,
                'message': 'first_name must been between 3 and 25'
            }
            raise ValidationError(data)
        return username
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))

        if instance.auth_status == VERIFIED:
            instance.auth_status = DONE
        instance.save()
        return instance
    
class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['userinput'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(read_only=True, required=False)

    def auth_validate(self, data):
        user_input = data.get('userinput')
        user_type = check_user_type(user_input)

        if user_type == "email":
            user = self.get_user(email__iexact=user_input)
            username = user.username
        elif user_type == "phone":
            user = self.get_user(phone__iexact=user_input)
            username = user.username
        elif user_type == "username":
            username = user_input
        else:
            data = {
                'success': False,
                'message': 'Sorry, login or password incorrect'
            }
            raise ValidationError(data)
        authencitation_kwargs = {
            self.username_field: username,
            'password': data['password']
        }

        current_user = User.objects.filter(username__iexact=username).first()
        if current_user is not None and current_user in [NEW, VERIFIED]:
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Siz royxatdan otmagansiz'
                }
            )
        user = authenticate(**authencitation_kwargs)
        if user is not None:
            self.user = user
        else:
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Sorry, login or password in correct'
                }
            )
    
    def validate(self, data):
        self.auth_validate(data)
        if self.user.auth_status != DONE:
            raise PermissionDenied('Siz royxatdan otmagansiz')
        data = self.user.token()
        data['auth_status'] = self.user.auth_status
        data['full_name'] = self.user.full_name
        return data

    def get_user(self, **kwargs):
        users = User.objects.filter(**kwargs)
        if not users.exists():
            raise ValidationError(
                {
                    'success': False,
                    'message': 'No active account Found'
                }
            )
        return users.first()