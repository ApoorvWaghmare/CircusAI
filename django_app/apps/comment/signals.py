from django.db.models.signals import post_save
from django.dispatch import receiver
import json

#----------#

from apps.aws.services import SNSService
from apps.notification.services import NotificationQueryService, NotificationAtomicService

#----------#

from .models.mysql_models import Comment

#------------------------------------------------------------------------------------------------------------------#

@receiver(post_save, sender = Comment)
def comment_notification(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        post = instance.post_id
        post_creator_user = post.user_id
        commented_by_user = instance.user_id
        # create subject
        subject = "Comment notification"
        # create message
        message = commented_by_user.username + " commented on your post"
        # create message attributes
        message_attributes = {
            'post_id': post.id,
        }
        endpoints_arn = SNSService().get_endpoints_arn_by_user_id(target_user_id = post_creator_user.id)
        print('Notification sending...')
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
        is_error = NotificationAtomicService.save_notification(user = post_creator_user,
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
