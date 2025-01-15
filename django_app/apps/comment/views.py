from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND

#----------#

from .services import CommentAtomicService, CommentQueryService
from .serializers import *

#======================================================================================================================#
# SaveCommentView
#======================================================================================================================#      

class SaveCommentView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        is_error = CommentAtomicService.save_comment(user_id = request.user.id,
                                                     post_id = request.data.pop('post_id'),
                                                     comment = request.data.pop('comment'))
        if is_error:
            return Response(False, status = HTTP_422_UNPROCESSABLE_ENTITY)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of SaveCommentView
#======================================================================================================================#

#======================================================================================================================#
# GetAllCommentsView
#======================================================================================================================#      

class GetAllCommentsView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = GetAllCommentsSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request, post_id: int) -> Response:
        if not post_id:
            return Response({"detail": "post_id is required"}, status = HTTP_400_BAD_REQUEST)

        comments = CommentQueryService.get_all_comments(post_id = post_id)
        
        # Now that comments have been retrieved, serialize them, no need to call is_valid()
        serializer = self.get_serializer(instance = comments, many = True)
        
        # Directly return the serialized data
        return Response(serializer.data, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of GetAllCommentsView
#======================================================================================================================#
