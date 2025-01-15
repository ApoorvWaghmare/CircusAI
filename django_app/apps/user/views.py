from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from jose import jwt
from rest_framework_simplejwt.tokens import RefreshToken
import base64
import json

#----------#

from .services import *
from .serializers import *
from django_app import settings

#======================================================================================================================#
# TokenPairView
#======================================================================================================================#

class TokenPairView(TokenObtainPairView):
    
    serializer_class = TokenSerializer
    
    #------------------------------------------------------------------------------------------------------------------#
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        try:
            serializer.is_valid(raise_exception = True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status = HTTP_200_OK)

#======================================================================================================================#
# End of TokenPairView
#======================================================================================================================#

#======================================================================================================================#
# UserCreateView
#======================================================================================================================#

class UserCreateView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            username = serializer.data['username']
            is_error = UserAtomicService.create_user(serializer.data)
            user = UserQueryService.get_user_from_username(username = username)

            if not is_error:
                return Response({"id": user.id}, status = HTTP_201_CREATED)
            else:
                return Response('User Could Not Be Created', status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(serializer.errors, status = HTTP_422_UNPROCESSABLE_ENTITY)

#======================================================================================================================#
# End of UserCreateView
#======================================================================================================================#

#======================================================================================================================#
# UserDeleteView
#======================================================================================================================#

class UserDeleteView(APIView):

    permission_classes = [IsAuthenticated]
    
    #------------------------------------------------------------------------------------------------------------------#

    def delete(self, request: Request, pk: int) -> Response:
        user = UserQueryService.get_user(pk)
        if user is None:
            return Response(False, status = HTTP_404_NOT_FOUND)

        is_error = UserAtomicService.delete_user(user)
    
        if not is_error:
            return Response(True, status = HTTP_200_OK)
        else:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

#======================================================================================================================#
# End of UserDeleteView
#======================================================================================================================#

#======================================================================================================================#
# UserProfileView
#======================================================================================================================#      

class UserProfileView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request, pk: int) -> Response:
        user = UserQueryService.get_user(pk)
        if user is None:
            return Response('User Does Not Exist', status = HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance = user, data = request.data, partial = True)

        if serializer.is_valid():
            return Response(serializer.data, status = HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status = HTTP_500_INTERNAL_SERVER_ERROR)
        
#======================================================================================================================#
# End of UserProfileView
#======================================================================================================================#

#======================================================================================================================#
# SignOutView
#======================================================================================================================#      

class SignOutView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    
    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of SignOutView
#======================================================================================================================#

#======================================================================================================================#
# SaveUserFollowRequestView
#======================================================================================================================#      

class SaveUserFollowRequestView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        status = UserFollowingAtomicService.save_follow_request(request.data)
        if status:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of SaveUserFollowRequestView
#======================================================================================================================#

#======================================================================================================================#
# GetUserFolloweesView
#======================================================================================================================#      

class GetUserFolloweesView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserFolloweesSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request, pk: int) -> Response:
        followees = UserQueryService.get_user_followees(pk)
        serializer = self.get_serializer(instance = followees, many = True)
        # No need to check `is_valid()` on read operations, it's used for writing/creating/updating
        return Response(serializer.data, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of GetUserFolloweesView
#======================================================================================================================#

#======================================================================================================================#
# SetUserInactiveView
#======================================================================================================================#      

class SetUserInactiveView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request, pk: int) -> Response:
        status = UserAtomicService.set_user_inactive(pk)
        if status:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of SetUserInactiveView
#======================================================================================================================#

#======================================================================================================================#
# SetUserActiveView
#======================================================================================================================#      

class SetUserActiveView(GenericAPIView):

    permission_classes = [AllowAny]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request, pk: int) -> Response:
        status = UserAtomicService.set_user_active(pk)
        if status:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of SetUserActiveView
#======================================================================================================================#

#======================================================================================================================#
# BlockUserView
#======================================================================================================================#      

class BlockUserView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        is_error = UserBlockAtomicService.block_user(blocked_user_id = request.data.pop('blocked_user_id'), 
                                                     blocked_by_user_id = request.data.pop('blocked_by_user_id'))
        if is_error:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of BlockUserView
#======================================================================================================================#

#======================================================================================================================#
# UnBlockUserView
#======================================================================================================================#      

class UnBlockUserView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        is_error = UserBlockAtomicService.unblock_user(blocked_user_id = request.data.pop('blocked_user_id'), 
                                                       blocked_by_user_id = request.user.id)
        if is_error:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of UnBlockUserView
#======================================================================================================================#


#======================================================================================================================#
# GetAllBlockedUsersView
#======================================================================================================================#      

class GetAllBlockedUsersView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = BlockedUserSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request) -> Response:
        users = UserBlockQueryService.get_all_blocked_users(request.user.id)
        serializer = self.get_serializer(instance = users, many = True)
        return Response(serializer.data, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of GetAllBlockedUsersView
#======================================================================================================================#

#======================================================================================================================#
# SearchUsersView
#======================================================================================================================#

class SearchUsersView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = SearchUsersSerializer

    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request: Request) -> Response:
        users = UserQueryService.search_users(request.GET.get('query'))
        serializer = self.get_serializer(instance = users, many = True)
        return Response(serializer.data, status = HTTP_200_OK)
    
#======================================================================================================================#
# End of SearchUsersView
#======================================================================================================================#

#======================================================================================================================#
# EditProfilePicView
#======================================================================================================================#      

class EditProfilePicView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request: Request) -> Response:
        print('Inside EditProfilePicView')
        print(request.FILES)
        is_error = UserAtomicService.edit_profile_pic(user_id = request.user.id,
                                                      image_file = request.FILES.get('image_file'))
        if is_error:
            return Response(False, status = HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(True, status = HTTP_200_OK)
        
#======================================================================================================================#
# End of EditProfilePicView
#======================================================================================================================#

#======================================================================================================================#
# AppleSignInView
#======================================================================================================================#
class AppleSignInView(APIView):

    
    # Set this to True for testing, False for production
    TEST_MODE = True

    #------------------------------------------------------------------------------------------------------------------#
    
    def decode_token(self, token):
        try:
            # Split the token into header, payload, and signature
            header, payload, signature = token.split('.')
            # Decode the payload
            payload += '=' * (-len(payload) % 4)  # Add padding
            decoded_payload = base64.urlsafe_b64decode(payload)
            payload_data = json.loads(decoded_payload)
            return payload_data
        except Exception as e:
            logger.error(f"Error decoding token: {str(e)}")
            return None
        
    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request):
        logger.info(f"AppleSignInView.TEST_MODE = {self.TEST_MODE}")
        
        identity_token = request.data.get('identity_token')
        if not identity_token:
            logger.error("Identity token is missing")
            return Response({'error': 'Identity token is required'}, status = HTTP_400_BAD_REQUEST)

        try:
            # Manually decode the token
            decoded_token = self.decode_token(identity_token)
            if not decoded_token:
                return Response({'error': 'Invalid token format'}, status = HTTP_400_BAD_REQUEST)
            
            logger.info(f"Decoded token: {decoded_token}")
            
            # Check if the token is expired
            if decoded_token['exp'] < time.time():
                logger.error("Token has expired")
                return Response({'error': 'Token has expired'}, status = HTTP_400_BAD_REQUEST)

            # Verify the issuer
            if decoded_token['iss'] != 'https://appleid.apple.com':
                logger.error(f"Invalid issuer: {decoded_token['iss']}")
                return Response({'error': 'Invalid issuer'}, status = HTTP_400_BAD_REQUEST)

            # Verify the audience only if not in test mode
            if not self.TEST_MODE:
                if decoded_token['aud'] != settings.APPLE_BUNDLE_ID:
                    logger.error(f"Invalid audience: {decoded_token['aud']}")
                    return Response({'error': 'Invalid audience'}, status = HTTP_400_BAD_REQUEST)
            else:
                logger.info("Skipping audience check in test mode")
            
            # Get the user's email and Apple's unique user ID
            email = decoded_token.get('email')
            apple_user_id = decoded_token.get('sub')

            if not email or not apple_user_id:
                logger.error("Missing email or apple_user_id in token payload")
                return Response({'error': 'Invalid token payload'}, status = HTTP_400_BAD_REQUEST)

            logger.info(f"Proceeding with email: {email} and apple_user_id: {apple_user_id}")

            # Check if user exists
            user = UserQueryService.get_user_from_email(email = email)

            if not user:
                # Create new user
                user_data = {
                    'username': str(email).replace('@', ''),
                    'email': email,
                    'password': 'password',
                    'bio_ref': ''
                }
                logger.info(f"Creating new user with data: {user_data}")
                is_error = UserAtomicService.create_user(user_data)
                if is_error:
                    logger.error("Failed to create user")
                    return Response({'error': 'User could not be created'}, status = HTTP_500_INTERNAL_SERVER_ERROR)
                user = UserQueryService.get_user_from_email(email = email)

            # Generate token
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id
            }
            logger.info(f"Successful sign in for user_id: {user.id}")
            return Response(response_data, status = HTTP_200_OK)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'An unexpected error occurred'}, status = HTTP_500_INTERNAL_SERVER_ERROR)
        
#======================================================================================================================#
# End of AppleSignInView
#======================================================================================================================#

#======================================================================================================================#
# GoogleSignInView
#======================================================================================================================#

class GoogleSignInView(APIView):
    
    # Set this to True for testing, False for production
    TEST_MODE = True

        
    #------------------------------------------------------------------------------------------------------------------#

    def post(self, request):
        logger.info(f"AppleSignInView.TEST_MODE = {self.TEST_MODE}")
        email = request.data.get('email')
        identity_token = request.data.get('id_token')
        user_id = request.data.get('user_id')
        if not identity_token:
            logger.error("Identity token is missing")
            return Response({'error': 'Identity token is required'}, status = HTTP_400_BAD_REQUEST)

        elif not user_id:
            logger.error("User ID is missing")
            return Response({'error': 'User ID is required'}, status = HTTP_400_BAD_REQUEST)
        try:


            # Check if user exists
            user = UserQueryService.get_user_from_username(username = user_id)

            if not user:
                # Create new user
                user_data = {
                    'username': user_id,
                    'email': email,
                    'password': identity_token,
                    'bio_ref': ''
                }
                logger.info(f"Creating new user with data: {user_data}")
                is_error = UserAtomicService.create_user(user_data)
                if is_error:
                    logger.error("Failed to create user")
                    return Response({'error': 'User could not be created'}, status = HTTP_500_INTERNAL_SERVER_ERROR)
                user = UserQueryService.get_user_from_username(email = user_id)

            # Generate token
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id
            }
            logger.info(f"Successful sign in for user_id: {user.id}")
            return Response(response_data, status = HTTP_200_OK)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'An unexpected error occurred'}, status = HTTP_500_INTERNAL_SERVER_ERROR)

#======================================================================================================================#
# End of GoogleSignInView
#======================================================================================================================#


#======================================================================================================================#
# UserActivityView
#======================================================================================================================#      

class UserActivityView(APIView):

    permission_classes = [AllowAny]

    #------------------------------------------------------------------------------------------------------------------#

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({"error": "Username or email is required"}, status=HTTP_400_BAD_REQUEST)

        activity_status = UserQueryService.check_user_activity(user_id)

        if activity_status is None:
            return Response({"error": "User not found"}, status=HTTP_404_NOT_FOUND)
        
        return Response({"is_active": activity_status}, status=HTTP_200_OK)
        
#======================================================================================================================#
# End of UserActivityView
#======================================================================================================================#

