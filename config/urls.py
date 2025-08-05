from django.contrib import admin
from django.urls import path, include

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Taskify API",
      default_version='v1',
      description="Taskify loyihasining API hujjatlari",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="leviackermanw71@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('task/', include('tasks.urls')),
    path('friends/', include('friends.urls')),
    path('groups/', include('group.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]