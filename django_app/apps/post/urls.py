from django.urls import path

#----------#

from .views import *

#----------#

urlpatterns = [
    path('create-text-2-image', CreatePostTxt2ImgView.as_view(), name = 'create-text-2-image'),
    path('create-text-image-2-image', CreatePostTxtImg2ImgView.as_view(), name = 'text-image-2-image'),
    path('create-text-face-2-image', CreatePostTxtFace2ImgView.as_view(), name = 'create-text-face-2-image'),
    path('<int:pk>/get-home-feed', HomeFeedView.as_view(), name = 'get-home-feed'),
    path('<int:pk>/get-search-feed', SearchFeedView.as_view(), name = 'get-home-feed'),
    path('<int:pk>/get-profile-feed', ProfileFeedView.as_view(), name = 'get-profile-feed'),
    path('report-post', PostReportView.as_view(), name = 'report-post'),
    path('publish-post', PublishPostView.as_view(), name = 'publish-post'),
    path('search-posts', SearchPostsView.as_view(), name = 'search-posts'),
    path('add-image-text', AddImageTextView.as_view(), name = 'add-image-text'),
    path('get-post', GetPostView.as_view(), name = 'get-post'),
    path('delete-post', DeletePostView.as_view(), name = 'delete-post'),
    path('upload-image', ImageUploadView.as_view(), name = 'upload-image'),
    path('generate-anime-prompt', GenerateAnimePromptView.as_view(), name='generate_anime_prompt'),
]
