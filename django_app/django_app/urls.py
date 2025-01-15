"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import health_check
urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/user/', include('apps.user.urls')),
    path('api/post/', include('apps.post.urls')),
    path('api/engagement/', include('apps.engagement.urls')),
    path('api/comment/', include('apps.comment.urls')),
    path('api/notification/', include('apps.notification.urls')),
    path('api/bookmark/', include('apps.bookmark.urls')),
    path('', health_check),  # Map root URL to health check view
]
