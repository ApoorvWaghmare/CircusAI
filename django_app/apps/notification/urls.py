from django.urls import path

#----------#

from .views import RegisterDeviceView, GetAllNotificationsView

#----------#

urlpatterns = [
    path('register-device', RegisterDeviceView.as_view(), name = 'register-device'),
    path('get-all-notifications', GetAllNotificationsView.as_view(), name = 'get-all-notifications'),
]