import logging
from django.db.models.query import QuerySet


#----------#

from apps.user.models.mysql_models import User
from apps.aws.services import SNSService
from utilities.custom import Service

#----------#

from .models import Notification

#----------#

logger = logging.getLogger(__name__)

#======================================================================================================================#
# NotificationAtomicService
#======================================================================================================================#

@Service.wrap
class NotificationAtomicService:

    service_type = 'Atomic'

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def save_notification(user: object, subject: str, message: str, message_attributes: str) -> None:
        notification = Notification(user_id = user, 
                                    subject = subject, 
                                    message = message, 
                                    message_attributes = message_attributes)
        notification.save()

#======================================================================================================================#
# End of NotificationAtomicService
#======================================================================================================================#

#======================================================================================================================#
# NotificationQueryService
#======================================================================================================================#

@Service.wrap
class NotificationQueryService:

    service_type = 'Query'
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_all_notifications(user_id: int) -> QuerySet:
        user = User.objects.get(pk = user_id)
        return Notification.objects.filter(user_id = user).order_by('-timestamp')

#======================================================================================================================#
# End of NotificationQueryService
#======================================================================================================================#
