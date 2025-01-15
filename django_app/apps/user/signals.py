from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import json

#----------#

from apps.aws.services import SNSService
from apps.notification.services import NotificationQueryService, NotificationAtomicService

#----------#

from .models.mysql_models import UserFollowing

#------------------------------------------------------------------------------------------------------------------#

@receiver(post_save, sender = UserFollowing)
def follow_request_notification(sender, instance, created, **kwargs):
    try:
        follower = instance.follower_id
        followee = instance.followee_id
        # create subject
        subject = "New follower added"
        # create message
        message = follower.username + " started following you"
        # create message attributes
        message_attributes = {
            'follower_id': follower.id,
        }
        endpoints_arn = SNSService().get_endpoints_arn_by_user_id(target_user_id = followee.id)
        for endpoint_arn in endpoints_arn:
            status = SNSService().publish_message(subject = subject,
                                                message = message,
                                                endpoint_arn = endpoint_arn,
                                                message_attributes = message_attributes)
            if status == True:
                print('Notification sent')
            else:
                print("Error is sending notfication")
        print('Saving notification...')
        is_error = NotificationAtomicService.save_notification(user = followee,
                                                            subject = subject,
                                                            message = message,
                                                            message_attributes = json.dumps(message_attributes))
        if is_error == False:
            print('Notification saved')
        else:
            print('Error in saving notification')
    except Exception as e:
        print(e)
        pass

#------------------------------------------------------------------------------------------------------------------#
