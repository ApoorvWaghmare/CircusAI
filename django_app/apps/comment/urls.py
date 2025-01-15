from django.urls import path

#----------#

from .views import *
    
#----------#

urlpatterns = [
    path('save-comment', SaveCommentView.as_view(), name = 'save-comment'),
    path('<int:post_id>/get-all-comments', GetAllCommentsView.as_view(), name = 'get-all-comments'),
]