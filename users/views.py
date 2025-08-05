from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, VIA_EMAIL, VIA_PHONE, NEW, VERIFIED, DONE
from .serializers import SignUpSerializer, ChangeUserInformationSerializer, LoginSerializer

class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

class VerifyView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(code, user)

        return Response(
            {
                'success': True,
                'message': 'User successfully created',
                'access_token': user.token()['access_token'],
                'refresh_token': user.token()['refresh_token']
            }
        )

    
    @staticmethod
    def check_verify(code, user):
        verifies = user.verify_codes.filter(code = code, expiration_time__gte = timezone.now(), is_confirmed=False)
        if not verifies.exists():
            data = {
                'success': False,
                'message': 'Code invalid'
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = VERIFIED
            user.save()
        return True
    
class ChangeUserInformationView(UpdateAPIView):
    serializer_class = ChangeUserInformationSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super(ChangeUserInformationView, self).update(request, *args, **kwargs)
        data = (
            {
                'success': True,
                'message': 'Malumotlar yangilandi',
                'auth_status': self.request.user.auth_status
            }
        )
        return Response(data, status=200)
    
    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInformationView, self).update(request, *args, **kwargs)
        data = (
            {
                'success': True,
                'message': 'Malumotlar yangilandi',
                'auth_status': self.request.user.auth_status
            }
        )
        return Response(data, status=200)
    
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]