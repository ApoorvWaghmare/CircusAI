from typing import Dict, Any
from django.utils import timezone
from django.db.models.query import QuerySet
from rest_framework.serializers import ModelSerializer
from bson import ObjectId

#----------#

from .models import mysql_models
from .models import mongo_models

#----------#

from apps.user.services import UserQueryService
from apps.post.services import PostQueryService
from utilities.custom import Service

#======================================================================================================================#
# CommentQueryService
#======================================================================================================================#

@Service.wrap
class CommentQueryService:

    service_type = 'Query'

    #------------------------------------------------------------------------------------------------------------------#
    @staticmethod
    def get_all_comments(post_id: int) -> QuerySet:
        post = PostQueryService.get_post(post_id)
        return mysql_models.Comment.objects.filter(post_id = post).order_by('-timestamp')

#======================================================================================================================#
# End of CommentQueryService
#======================================================================================================================#


#======================================================================================================================#
# CommentAtomicService
#======================================================================================================================#

@Service.wrap
class CommentAtomicService:

    service_type = 'Atomic'
      
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def save_comment(user_id: int, post_id: int, comment: str) -> None:
        # write in MySQL
        post = PostQueryService.get_post(post_id)
        user = UserQueryService.get_user(user_id)
        temp_comment = mysql_models.Comment(post_id = post, user_id = user)
        temp_comment.save()
        # write in MongoDB
        comment_ref = mongo_models.Comment.save_comment(comment = comment, user_id = user_id, post_id = post_id)
        # update in MySQL
        temp_comment.comment_ref = comment_ref
        temp_comment.save(update_fields = ['comment_ref'])

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def save_serializer(serializer: ModelSerializer) -> None:
        serializer.save()

#======================================================================================================================#
# End of CommentAtomicService
#======================================================================================================================#