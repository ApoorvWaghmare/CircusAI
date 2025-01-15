from typing import Dict, Any
from rest_framework.serializers import ModelSerializer
from django.db.models.query import QuerySet
from django.db.models.functions import Now
from datetime import timedelta
from django.db.models import Count

#----------#

from .models import Engagement

#----------#

from apps.user.services import UserQueryService
from apps.post.models.mysql_models import Post
from utilities.custom import Service

#======================================================================================================================#
# EngagementQueryService
#======================================================================================================================#

@Service.wrap
class EngagementQueryService:

    service_type = 'Query'

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_most_liked_posts(days: int) -> QuerySet:
        recent_engagements = Engagement.objects.filter(engagement_type = Engagement.EngagementType.LIKE,
                                                       timestamp__gte = Now() - timedelta(days = days))
        return recent_engagements.values('post_id').annotate(total_likes = Count('id')).order_by('-total_likes')

#======================================================================================================================#
# End of EngagementQueryService
#======================================================================================================================#

#======================================================================================================================#
# EngagementAtomicService
#======================================================================================================================#

@Service.wrap
class EngagementAtomicService:

    service_type = 'Atomic'

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def create_engagement(user: object, post: object, engagement_type: str) -> None:
        engagement = Engagement(post_id = post, user_id = user, engagement_type = engagement_type)
        engagement.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def update_engagement(user: object, post: object, engagement_type: str) -> None:
        engagement = Engagement.objects.get(post_id = post, user_id = user)
        engagement.engagement_type = engagement_type
        engagement.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def handle_engagement(user_id: int, post_id: int, engagement_type: str) -> None:
        user = UserQueryService.get_user(user_id)
        post = Post.objects.get(pk = post_id)
        try:
            engagement = Engagement.objects.get(post_id = post, user_id = user)
            if ( engagement.engagement_type != engagement_type ):
                EngagementAtomicService.update_engagement(user, post, engagement_type)
        except:
            EngagementAtomicService.create_engagement(user, post, engagement_type)

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def delete_engagement(user_id: int, post_id: int) -> None:
        post = Post.objects.get(pk = post_id)
        user = UserQueryService.get_user(user_id)
        Engagement.objects.filter(post_id = post, user_id = user).delete()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def save_serializer(serializer: ModelSerializer) -> None:
        serializer.save()

#======================================================================================================================#
# End of EngagementAtomicService
#======================================================================================================================#