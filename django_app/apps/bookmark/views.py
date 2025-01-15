from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND
from rest_framework import status

#----------#

from .services import BookmarkQueryService, BookmarkAtomicService
from apps.post.serializers import PostSerializer
from apps.user.services import UserQueryService
from apps.post.services import PostQueryService


#======================================================================================================================#
# BookmarkView
#======================================================================================================================#

class BookmarkView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get(request) -> Response:
        bookmarked_posts = BookmarkQueryService.get_all_bookmarks(request.user.id)
        # Serialize the posts
        serialized_posts = PostSerializer(bookmarked_posts, many = True)
        # Return the serialized data as a response
        return Response(serialized_posts.data)

#======================================================================================================================#
# End of BookmarkView
#======================================================================================================================#

#======================================================================================================================#
# AddBookmarkView
#======================================================================================================================#

class AddBookmarkView(GenericAPIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = UserQueryService.get_user(request.user.id)
            post_id = request.data.pop('post_id')
            post = PostQueryService.get_post(post_id)

            if not post:
                return Response({'error': 'Post not found.'}, status = status.HTTP_404_NOT_FOUND)

            BookmarkAtomicService.add_bookmark(user, post)
            return Response({'success': 'Bookmark added successfully.'}, status = status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)

#======================================================================================================================#
# End of AddBookmarkView
#======================================================================================================================#

#======================================================================================================================#
# DeleteBookmarkView
#======================================================================================================================#

class DeleteBookmarkView(GenericAPIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = UserQueryService.get_user(request.user.id)
            post_id = request.data.get('post_id')
            post = PostQueryService.get_post(post_id)

            if not post:
                return Response({'error': 'Post not found.'}, status = status.HTTP_404_NOT_FOUND)

            BookmarkAtomicService.delete_bookmark(user, post)
            return Response({'success': 'Bookmark deleted successfully.'}, status = status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)

#======================================================================================================================#
# End of DeleteBookmarkView
#======================================================================================================================#