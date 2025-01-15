from typing import Dict, Any
from django.utils import timezone
from django.db.models.query import QuerySet, EmptyQuerySet
from rest_framework.serializers import ModelSerializer
from django.db.models import Q
import os
import time
import random
import string
from PIL import Image

#----------#

from utilities.custom import Service
from apps.aws.services import S3Service

#----------#

from .models.mysql_models import User, UserFollowing, UserBlock
from .models.mongo_models import Bio

#======================================================================================================================#
# UserQueryService
#======================================================================================================================#

@Service.wrap
class UserQueryService:

    service_type = 'Query'

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_user_from_username(username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist:
            return None
        
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_user_from_email(email):
        try:
            return User.objects.get(email = email)
        except User.DoesNotExist:
            return None
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def check_username_existence(username: str) -> bool:
        return User.objects.filter(username = username).exists()  
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_user(pk: int) -> User:
        return User.objects.get(pk = pk)
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_user_from_username(username: str) -> User:
        return User.objects.get(username = username)
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_username(pk: int) -> str:
        user = User.objects.get(pk = pk)
        return user.username
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_user_followees(pk: int) -> User:
        followee_id_query_set = UserFollowingQueryService.get_user_followee_ids(pk)
        followees = User.objects.filter(id__in = followee_id_query_set)
        return followees
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def exclude(primary_queryset: QuerySet, exclude_queryset: QuerySet) -> QuerySet:
        return User.objects.filter(id__in = primary_queryset).exclude(id__in = exclude_queryset)
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def search_users(query: str) -> QuerySet:
        if query == '' or query == None:
            return EmptyQuerySet()
        else:
            return User.objects.filter(Q(first_name__icontains = query) |
                                       Q(last_name__icontains = query) |
                                       Q(username__icontains = query) ).order_by('-last_login')
        
    #------------------------------------------------------------------------------------------------------------------#
        
    @staticmethod
    def check_user_activity(user_id: int) -> bool:
        user = UserQueryService.get_user(user_id)
        if user is None:
            return None
        is_active = user.is_active
        return is_active

#======================================================================================================================#
# End of UserQueryService
#======================================================================================================================#

#======================================================================================================================#
# UserAtomicService
#======================================================================================================================#

@Service.wrap
class UserAtomicService:

    service_type = 'Atomic'
      
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def create_user(data: Dict[str, Any]) -> None:
        # write in MySQL  
        password = data.pop('password')
        bio_ref = data.pop('bio_ref')
        user = User(**data)
        user.set_password(password)
        user.save()
        # write in MongoDB
        bio_id = Bio.save_bio(bio = bio_ref, user_id = user.id)
        # update in MySQL
        user.bio_ref = bio_id
        user.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def save_serializer(serializer: ModelSerializer) -> None:
        serializer.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def delete_user(user: User) -> None:
        user.delete()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def set_last_login(user: User) -> None:
        user.last_login = timezone.now()
        user.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def set_user_inactive(pk: int) -> None:
        user = UserQueryService.get_user(pk)
        user.is_active = 0
        user.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def set_user_active(pk: int) -> None:
        user = UserQueryService.get_user(pk)
        user.is_active = 1
        user.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def edit_profile_pic(user_id: int, image_file: object) -> None:
        # get user
        user = User.objects.get(pk = user_id)
        # save image to temp folder and resize
        image_path = os.path.join('/home/ubuntu/CircusAI/application/backend/ai_engine/medias',
                                  str(user_id) + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) + str(time.time()) + '.png')
        image = Image.open(image_file)
        image = image.resize((1024, 1024))
        image.save(image_path)
        # upload image to S3
        s3_service = S3Service()
        if user.profile_pic_ref != None:
            s3_service.delete(key = user.profile_pic_ref)
        user.profile_pic_ref = s3_service.upload(local_path = image_path)
        user.save()

#======================================================================================================================#
# End of UserAtomicService
#======================================================================================================================#

#======================================================================================================================#
# UserFollowingQueryService
#======================================================================================================================#

@Service.wrap
class UserFollowingQueryService:

    service_type = 'Query'
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_user_followee_ids(pk: int) -> QuerySet:
        return UserFollowing.objects.filter(follower_id_id = pk).values_list('followee_id_id', flat=True)
    

#======================================================================================================================#
# End of UserFollowingQueryService
#======================================================================================================================#

#======================================================================================================================#
# UserFollowingAtomicService
#======================================================================================================================#

@Service.wrap
class UserFollowingAtomicService:

    service_type = 'Atomic'
      
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def save_follow_request(data: Dict[str, Any]) -> None:
        follower = UserQueryService.get_user(pk = data.pop('follower_id'))
        followee = UserQueryService.get_user(pk = data.pop('followee_id'))
        user_following = UserFollowing(follower_id = follower, followee_id = followee)
        user_following.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def save_serializer(serializer: ModelSerializer) -> None:
        serializer.save()

#======================================================================================================================#
# End of UserFollowingAtomicService
#======================================================================================================================#

#======================================================================================================================#
# UserBlockQueryService
#======================================================================================================================#

@Service.wrap
class UserBlockQueryService:

    service_type = 'Query'
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_blocked_user_ids(blocked_by_user_id: int) -> QuerySet:
        blocked_by_user = UserQueryService.get_user(blocked_by_user_id)
        user_blocks = UserBlock.objects.filter(blocked_by_user_id = blocked_by_user)
        return user_blocks.values_list('blocked_user_id', flat = True)

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_blocked_users(blocked_by_user_id: int) -> QuerySet:
        blocked_by_user = UserQueryService.get_user(blocked_by_user_id)
        user_blocks = UserBlock.objects.filter(blocked_by_user_id = blocked_by_user)

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_all_blocked_users(pk: int) -> QuerySet:
        user = UserQueryService.get_user(pk)
        blocked_user_ids = UserBlock.objects.filter(blocked_by_user_id = user).values_list('blocked_user_id', flat = True)
        return User.objects.filter(id__in = blocked_user_ids)

#======================================================================================================================#
# End of UserBlockQueryService
#======================================================================================================================#

#======================================================================================================================#
# UserBlockAtomicService
#======================================================================================================================#

@Service.wrap
class UserBlockAtomicService:

    service_type = 'Atomic'
      
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def save_serializer(serializer: ModelSerializer) -> None:
        serializer.save()
        
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def block_user(blocked_user_id: int, blocked_by_user_id: int) -> None:
        user_block = UserBlock(blocked_user_id = UserQueryService.get_user(blocked_user_id), 
                               blocked_by_user_id = UserQueryService.get_user(blocked_by_user_id))
        user_block.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def unblock_user(blocked_user_id: int, blocked_by_user_id: int) -> None:
        blocked_by_user = UserQueryService.get_user(blocked_by_user_id)
        blocked_user = UserQueryService.get_user(blocked_user_id)
        block = UserBlock.objects.filter(blocked_user_id = blocked_user, blocked_by_user_id = blocked_by_user)
        block.delete()


#======================================================================================================================#
# End of UserBlockAtomicService
#======================================================================================================================#