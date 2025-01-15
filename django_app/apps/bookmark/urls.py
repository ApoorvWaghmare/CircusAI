from django.urls import path

#----------#

from .views import *

#----------#

urlpatterns = [
    path('get-bookmarked-posts', BookmarkView.as_view(), name = 'get-bookmarked-posts'),
    path('add-bookmark', AddBookmarkView.as_view(), name = 'add-bookmark'),
    path('delete-bookmark', DeleteBookmarkView.as_view(), name = 'delete-bookmark'),
]