from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK

#----------#

from apps.aws.services import SNSService

#----------#

from .services import NotificationQueryService
from .serializers import NotificationSerializer

#======================================================================================================================#
# RegisterDeviceView
#======================================================================================================================#      

class RegisterDeviceView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        status = SNSService().register_device(device_token = request.data.pop('device_token'), 
                                              user_id = request.user.id)   
        if status == False:
            return Response(False, status = HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(True, status = HTTP_200_OK)
            
        
#======================================================================================================================#
# End of RegisterDeviceView
#======================================================================================================================#

#======================================================================================================================#
# GetAllNotificationsView
#======================================================================================================================#      

class GetAllNotificationsView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request) -> Response:
        notifications = NotificationQueryService.get_all_notifications(user_id = request.user.id)
        serializer = self.get_serializer(instance = notifications, many = True)
        return Response(serializer.data, status = HTTP_200_OK)
            
#======================================================================================================================#
# End of GetAllNotificationsView
#======================================================================================================================#
