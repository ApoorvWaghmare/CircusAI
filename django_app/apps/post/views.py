from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND

#----------#

from .services import CreatePostService, PostQueryService, PostReportService, PostAtomicService, GeminiTextGeneratorService
from .serializers import PostSerializer, SearchPostsSerializer
from .pagintations import *

#======================================================================================================================#
# CreatePostTxt2ImgView
#======================================================================================================================#

class CreatePostTxt2ImgView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    
    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        prompt = request.data.pop('prompt')
        width = request.data.pop('width', 512)
        height = request.data.pop('height', 512)
        post = CreatePostService.text_2_image(user_id = 168, prompt = prompt, width = width, height = height )
        serializer = self.get_serializer(instance = post, data = request.data, partial = True)
        if serializer.is_valid():
            return Response(serializer.data, status = HTTP_200_OK)
        else:
            return Response(serializer.errors, status = HTTP_500_INTERNAL_SERVER_ERROR)

#======================================================================================================================#
# End of CreatePostTxt2ImgView
#======================================================================================================================#

#======================================================================================================================#
# CreatePostTxtImg2ImgView
#======================================================================================================================#

class CreatePostTxtImg2ImgView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        user_id = request.user.id
        prompt = request.data.pop('prompt')
        ref_post_id = request.data.pop('ref_post_id')
        width = request.data.pop('width', 1024)
        length = request.data.pop('length', 1024)
        createpostinstance = CreatePostService()
        post = createpostinstance.text_image_2_image(user_id = user_id, 
                                                    prompt = prompt, 
                                                    ref_post_id = ref_post_id,
                                                    width = width, 
                                                    length = length)
        serializer = self.get_serializer(instance = post, data = request.data, partial = True)
        if serializer.is_valid():
            return Response(serializer.data, status = HTTP_200_OK)
        else:
            return Response(serializer.errors, status = HTTP_500_INTERNAL_SERVER_ERROR)

#======================================================================================================================#
# End of CreatePostTxtImg2ImgView
#======================================================================================================================#

#======================================================================================================================#
# CreatePostTxtFace2ImgView
#======================================================================================================================#

class CreatePostTxtFace2ImgView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        post = CreatePostService.text_face_2_image(user_id = request.user.id,
                                                   prompt = request.GET.get('prompt'), 
                                                   face_image_file = request.FILES.get('face_image_file'))
        serializer = self.get_serializer(instance = post, data = request.data, partial = True)
        if serializer.is_valid():
            return Response(serializer.data, status = HTTP_200_OK)
        else:
            return Response(serializer.errors, status = HTTP_500_INTERNAL_SERVER_ERROR)

#======================================================================================================================#
# End of CreatePostTxtFace2ImgView
#======================================================================================================================#

#======================================================================================================================#
# HomeFeedView
#======================================================================================================================#

class HomeFeedView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = HomeFeedPagination
    
    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request, pk: int) -> Response:
        feed = PostQueryService.get_home_feed(pk)
        feed = self.paginate_queryset(feed)
        serializer = self.get_serializer(instance = feed, many = True)
        response = self.get_paginated_response(serializer.data)
        return response

#======================================================================================================================#
# End of HomeFeedView
#======================================================================================================================#

#======================================================================================================================#
# SearchFeedView
#======================================================================================================================#

class SearchFeedView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = SearchFeedPagination
    
    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request, pk: int) -> Response:
        feed = PostQueryService.get_search_feed(pk)
        feed = self.paginate_queryset(feed)
        serializer = self.get_serializer(instance = feed, many = True)
        return self.get_paginated_response(serializer.data)

#======================================================================================================================#
# End of SearchFeedView
#======================================================================================================================#

#======================================================================================================================#
# ProfileFeedView
#======================================================================================================================#

class ProfileFeedView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = ProfileFeedPagination
    
    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request, pk: int) -> Response:
        print(request.user)
        feed = PostQueryService.get_profile_feed(pk)
        feed = self.paginate_queryset(feed)
        serializer = self.get_serializer(instance = feed, many = True)
        return self.get_paginated_response(serializer.data)

#======================================================================================================================#
# End of ProfileFeedView
#======================================================================================================================#

#======================================================================================================================#
# GetPostView
#======================================================================================================================#

class GetPostView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    
    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request) -> Response:
        post = PostQueryService.get_post(request.GET.get('post_id'))
        serializer = self.get_serializer(instance = post, many = False)
        return Response(serializer.data, status = HTTP_200_OK)

#======================================================================================================================#
# End of GetPostView
#======================================================================================================================#

#======================================================================================================================#
# PostReportView
#======================================================================================================================#      

class PostReportView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        status = PostReportService.report_post(request.data)
        if status:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of PostReportView
#======================================================================================================================#

#======================================================================================================================#
# PublishPostView
#======================================================================================================================#      

class PublishPostView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        post_id = request.data.pop('post_id')
        caption = request.data.pop('caption')
        status = PostAtomicService.add_caption(post_id, caption)
        if status:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)
        
        status = PostAtomicService.update_post_visibiility(post_id)
        if status:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of PublishPostView
#======================================================================================================================#

#======================================================================================================================#
# SearchPostsView
#======================================================================================================================#

class SearchPostsView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = SearchPostsSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request) -> Response:
        users = PostQueryService.search_posts(request.GET.get('query'))
        serializer = self.get_serializer(instance = users, many = True)
        return Response(serializer.data, status = HTTP_200_OK)
    
#======================================================================================================================#
# End of SearchPostsView
#======================================================================================================================#

#======================================================================================================================#
# AddImageTextView
#======================================================================================================================#      

class AddImageTextView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        is_error = PostAtomicService.add_image_text(text = request.data.pop('text'),
                                                    text_attributes = request.data.pop('text_attributes'),
                                                    post_id = request.data.pop('post_id'))
        if is_error:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of AddImageTextView
#======================================================================================================================#

#======================================================================================================================#
# DeletePostView
#======================================================================================================================#      

class DeletePostView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        is_error = PostAtomicService.delete_post(post_id = request.data.pop('post_id'))
        if is_error:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of DeletePostView
#======================================================================================================================#

#======================================================================================================================#
# UploadImagePostView
#======================================================================================================================#

class ImageUploadView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    
    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        url = CreatePostService.upload_image(image_file = request.FILES.get('face_image_file'))
        return Response(url, status = HTTP_200_OK)

#======================================================================================================================#
# End of UploadImagePostView
#======================================================================================================================#

#======================================================================================================================#
# RandomAnimePrompt
#======================================================================================================================#

class GenerateAnimePromptView(GenericAPIView):
    def get(self, request):
        """Handle GET requests to generate an anime-style image prompt"""
        try:
            # Use the service to generate the anime prompt
            generated_prompt = GeminiTextGeneratorService.generate_anime_prompt()

            # Return the generated prompt as a JSON response
            return Response ({'prompt': generated_prompt}, status=200)
        
        except Exception as e:
            # Handle any errors and return an error message
            return Response ({'error': str(e)}, status=500)
        
#======================================================================================================================#
# End of RandomAnimePrompt
#======================================================================================================================#
