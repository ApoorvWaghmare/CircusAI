from django.urls import path

#----------#

from .views import HandleEngagementView, DeleteEngagementView

#----------#

urlpatterns = [
    path('handle-engagement', HandleEngagementView.as_view(), name = 'handle-engagement'),
    path('delete-engagement', DeleteEngagementView.as_view(), name = 'delete-engagement'),
]