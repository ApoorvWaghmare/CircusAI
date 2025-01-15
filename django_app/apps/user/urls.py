from django.urls import path, include

#----------#

from .views import *
    
#----------#

urlpatterns = [
    path('<int:pk>/delete', UserDeleteView.as_view(), name = 'auth-users-delete'),
    path('<int:pk>/profile', UserProfileView.as_view(), name = 'auth-users-details'),
    path('sign-in', TokenPairView.as_view(), name = 'auth-sign-in'),
    path('sign-up', UserCreateView.as_view(), name = 'auth-sign-up'),
    path('sign-out', SignOutView.as_view(), name = 'auth-sign-out'),
    path('user-follow-request', SaveUserFollowRequestView.as_view(), name = 'user-follow-request'),
    path('<int:pk>/get-user-followees', GetUserFolloweesView.as_view(), name = 'get-user-followees'),
    path('<int:pk>/set-user-inactive', SetUserInactiveView.as_view(), name = 'set-user-inactive'),
    path('<int:pk>/set-user-active', SetUserActiveView.as_view(), name = 'set-user-active'),
    path('accounts/', include('allauth.urls')),
    path('get-all-blocked-users', GetAllBlockedUsersView.as_view(), name = 'get-all-blocked-users'),
    path('block-user', BlockUserView.as_view(), name = 'block-user'),
    path('unblock-user', UnBlockUserView.as_view(), name = 'unblock-user'),
    path('search-users', SearchUsersView.as_view(), name = 'search-users'),
    path('edit-profile-pic', EditProfilePicView.as_view(), name = 'edit-profile-pic'),
    path('apple-sign-in', AppleSignInView.as_view(), name='auth-apple-sign-in'),
    path('check-user-activity', UserActivityView.as_view(), name='auth-apple-sign-in'),
    path('google-sign-in', GoogleSignInView.as_view(), name='auth-google-sign-in'),
]