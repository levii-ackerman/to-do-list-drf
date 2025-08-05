from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('task/', include('tasks.urls')),
    path('friends/', include('friends.urls')),
    path('groups/', include('group.urls')),
]
