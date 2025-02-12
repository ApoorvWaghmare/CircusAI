from django.db import models
from django.db.models import CharField, DateTimeField, OneToOneField, ForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

#----------#

from apps.user.models.mysql_models import User

#======================================================================================================================#
# NotificationManager
#======================================================================================================================#

class NotificationManager(models.Manager):
    
    #------------------------------------------------------------------------------------------------------------------#

    def create_notification(self):
        pass

#======================================================================================================================#
# End of NotificationManager
#======================================================================================================================#

#======================================================================================================================#
# Notification
#======================================================================================================================#

class Notification(models.Model):
    
    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        db_table = 'notification'

    #------------------------------------------------------------------------------------------------------------------#

    objects = NotificationManager()

    #------------------------------------------------------------------------------------------------------------------#
    
    user_id = ForeignKey(User, on_delete = models.CASCADE, related_name = 'user', null = False)
    subject = CharField(max_length = 255, null = False)
    message = CharField(max_length = 255, null = False)
    message_attributes = CharField(max_length = 255)
    timestamp = DateTimeField(auto_now_add = True)

    USER_ID = 'user_id'

#======================================================================================================================#
# End of Notification
#======================================================================================================================#