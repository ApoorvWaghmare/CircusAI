import logging
from typing import Dict, Any
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#----------#

from apps.aws.services import CloudfrontService
from .models.mysql_models import User, UserFollowing
from .models.mongo_models import Bio
from .services import UserAtomicService

#----------#

logger = logging.getLogger(__name__)

#======================================================================================================================#
# UserAllSerializer
#======================================================================================================================#

class UserAllSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

#======================================================================================================================#
# End of UserAllSerializer
#======================================================================================================================#

#======================================================================================================================#
# UserCreateSerializer
#======================================================================================================================#

class UserCreateSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "email",
                  "birth_date",
                  "username",
                  "gender",
                  "latitude",
                  "longitude",
                  "bio_ref",
                  "password"]

#======================================================================================================================#
# End of UserCreateSerializer
#======================================================================================================================#

#======================================================================================================================#
# UserProfileSerializer
#======================================================================================================================#

class UserProfileSerializer(ModelSerializer):

    #------------------------------------------------------------------------------------------------------------------#

    bio_ref = SerializerMethodField()
    profile_pic_ref = SerializerMethodField()

    #------------------------------------------------------------------------------------------------------------------#
    
    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "email",
                  "birth_date",
                  "username",
                  "gender",
                  "latitude",
                  "longitude",
                  "bio_ref",
                  "profile_pic_ref"]
        
    #------------------------------------------------------------------------------------------------------------------#
        
    def get_bio_ref(self, obj):
        try:
            bio_id = obj.bio_ref
            print(bio_id)
            bio_document = Bio.objects.get(id = bio_id)
            bio = bio_document.bio
            print("got bio from bio_ref",  bio)
            return bio
        except Exception as e:
            print(e)
            return None
        
    #------------------------------------------------------------------------------------------------------------------#
        
    def get_profile_pic_ref(self, obj):
        try:
            return CloudfrontService().create_signed_url(s3_object_key = obj.profile_pic_ref)
        except Exception as e:
            print(e)
            return None

#======================================================================================================================#
# End of UserProfileSerializer
#======================================================================================================================#

#======================================================================================================================#
# TokenSerializer
#======================================================================================================================#

class TokenSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)
       
        is_error = UserAtomicService.set_last_login(self.user)

        if is_error:
            logger.error(f'ERROR: Updating last_login for {self.user.username} ({self.user.id})')
        
        data['user_id'] = self.user.id
        return data

#======================================================================================================================#
# End of TokenSerializer
#======================================================================================================================#

#======================================================================================================================#
# UserFolloweesSerializer
#======================================================================================================================#

class UserFolloweesSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username']

#======================================================================================================================#
# End of UserFolloweesSerializer
#======================================================================================================================#

#======================================================================================================================#
# BlockedUserSerializer
#======================================================================================================================#

class BlockedUserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id",
                  "first_name",
                  "last_name",
                  "username",
                  "profile_pic_ref"]

#======================================================================================================================#
# End of BlockedUserSerializer
#======================================================================================================================#


#======================================================================================================================#
# UserCommentSerializer
#======================================================================================================================#

class UserCommentSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id",
                  "username",
                  "profile_pic_ref"]

#======================================================================================================================#
# End of UserCommentSerializer
#======================================================================================================================#

#======================================================================================================================#
# SearchUsersSerializer
#======================================================================================================================#

class SearchUsersSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id",
                  "username",
                  "first_name",
                  "last_name",
                  "profile_pic_ref"]

#======================================================================================================================#
# End of SearchUserSerializer
#======================================================================================================================#
