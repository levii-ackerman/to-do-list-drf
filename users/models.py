import random
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from shared.models import BaseModel
from datetime import timedelta

NEW, VERIFIED, DONE = "new", "verified", "done"
VIA_EMAIL, VIA_PHONE = "via_email", "via_phone"

class User(BaseModel, AbstractUser):
    AUTH_STATUS = (
        (NEW, NEW),
        (VERIFIED, VERIFIED),
        (DONE, DONE)
    )
    AUTH_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    auth_status = models.CharField(max_length=30, choices=AUTH_STATUS, default=NEW)
    auth_type = models.CharField(max_length=30, choices=AUTH_TYPE, default=VIA_EMAIL)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=30, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f"username - {self.username}"
    
    @property
    def full_name(self):
        return f"first_name - {self.first_name}. last_name - {self.last_name}"
    
    def create_code(self, verify_type):
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        UserConfirmation.objects.create(
            user_id = self.id,
            code = code,
            verify_type = verify_type
        )
        return code
    
    def check_username(self):
        if not self.username:
            temp_username = f"username-{uuid.uuid4().__str__().split('-')[1]}"
            while User.objects.filter(username = temp_username).exists():
                temp_username = f"{temp_username}{random.randint(0, 9)}"
            self.username = temp_username
    def check_pass(self):
        if not self.password:
            temp_passwrod = f"password-{uuid.uuid4().__str__().split('-')[1]}"
            self.password = temp_passwrod
    def hashing_pass(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
    def check_email(self):
        if self.email:
            normalized_email = self.email.lower()
            self.email = normalized_email
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
    def clean(self):
        self.check_username()
        self.check_pass()
        self.hashing_pass()
        self.check_email()
    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)
    

EMAIL_EXPER = 5
PHONE_EXPER = 2

class UserConfirmation(BaseModel):
    VERIFY_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='verify_codes')
    code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)
    verify_type = models.CharField(max_length=30, choices=VERIFY_TYPE)

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expiration_time = timezone.now() + timedelta(minutes=EMAIL_EXPER)
        elif self.verify_type == VIA_PHONE:
            self.expiration_time = timezone.now() + timedelta(minutes=PHONE_EXPER)
        super(UserConfirmation, self).save(*args, **kwargs)