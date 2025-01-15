from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND

#----------#

from .services import EngagementQueryService, EngagementAtomicService
from .serializers import *

#======================================================================================================================#
# HandleEngagementView
#======================================================================================================================#

class HandleEngagementView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = EngagementSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data = request.data)
        
        if serializer.is_valid():
            is_error = EngagementAtomicService.handle_engagement(user_id = request.user.id,
                                                                 post_id = request.data.pop('post_id'),
                                                                 engagement_type = request.data.pop('engagement_type'))
            if not is_error:
                return Response('Engagement Added', status = HTTP_201_CREATED)

            else:
                return Response('Engagement Could Not Be Added', status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(serializer.errors, status = HTTP_422_UNPROCESSABLE_ENTITY)

#======================================================================================================================#
# End of HandleEngagementView
#======================================================================================================================#

#======================================================================================================================#
# DeleteEngagementView
#======================================================================================================================#

class DeleteEngagementView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DeleteEngagementSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data = request.data)
        
        if serializer.is_valid():
            is_error = EngagementAtomicService.delete_engagement(user_id = request.user.id,
                                                                 post_id = request.data.pop('post_id'))
            if not is_error:
                return Response('Engagement Deleted', status = HTTP_201_CREATED)

            else:
                return Response('Engagement Could Not Be Deleted', status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(serializer.errors, status = HTTP_422_UNPROCESSABLE_ENTITY)

#======================================================================================================================#
# End of DeleteEngagementView
#======================================================================================================================#

