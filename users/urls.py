from django.urls import path
from .views import SignUpView, VerifyView, ChangeUserInformationView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('change-user-information/', ChangeUserInformationView.as_view(), name='change-user-information'),
]