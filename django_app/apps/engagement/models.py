from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from django.db.models import ForeignKey, DateTimeField

#----------#

from apps.post.models.mysql_models import Post
from apps.user.models.mysql_models import User

#======================================================================================================================#
# EngagementManager
#======================================================================================================================#

class EngagementManager(models.Manager):
    
    #------------------------------------------------------------------------------------------------------------------#

    def create_post(self):
        pass

#======================================================================================================================#
# End of EngagementManager
#======================================================================================================================#

#======================================================================================================================#
# Engagement
#======================================================================================================================#

class Engagement(models.Model):
    
    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        db_table = 'engagement'
        unique_together = ('post_id', 'user_id')

    #------------------------------------------------------------------------------------------------------------------#

    class EngagementType(models.TextChoices):
        LIKE = 'L', _('Like')
        DISLIKE = 'D', _('Dislike')

    #------------------------------------------------------------------------------------------------------------------#

    objects = EngagementManager()

    #------------------------------------------------------------------------------------------------------------------#

    post_id = ForeignKey(Post, on_delete = models.CASCADE, null = False, related_name = 'post_engagement')
    user_id = ForeignKey(User, on_delete = models.CASCADE, null = False, related_name = 'user_engagement')
    timestamp = DateTimeField(auto_now_add = True)
    engagement_type = CharField(max_length = 1, choices = EngagementType.choices, null = False)

    POST_ID = 'post_id'
    USER_ID = 'user_id'

#======================================================================================================================#
# End of Engagement
#======================================================================================================================#