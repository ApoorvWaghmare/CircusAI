from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
import json

#----------#

from apps.aws.services import SNSService
from apps.notification.services import NotificationQueryService, NotificationAtomicService

#----------#

from .models.mysql_models import Post

#----------#

# AI service custom signal
post_created = Signal()

#------------------------------------------------------------------------------------------------------------------#

@receiver(post_created)
def handle_post_created(sender: object, **kwargs):
    try:
        post = sender
        user = kwargs.get('user')
        print('Post created signal received')
        print(post)
        print(user)

        # create subject
        subject = "Creation ready!"
        # create message
        message = "A new image has been created"
        # create message attributes
        message_attributes = {
            'post_id': post.id,
        }

        endpoints_arn = SNSService().get_endpoints_arn_by_user_id(target_user_id = user.id)

        for endpoint_arn in endpoints_arn:
        
            if endpoint_arn is None:
                print(f"No endpoint ARN found for user {user.id}. Skipping notification.")
            else:
                status = SNSService().publish_message(subject = subject,
                                                    message = message,
                                                    endpoint_arn = endpoint_arn,
                                                    message_attributes = message_attributes)
                
                if status:
                    print('Notification sent')
                else:
                    print("Error in sending notification")

        print('Saving notification...')
        is_error = NotificationAtomicService.save_notification(user = user,
                                                            subject = subject,
                                                            message = message,
                                                            message_attributes = json.dumps(message_attributes))
        
        if not is_error:
            print('Notification saved')
        else:
            print('Error in saving notification')

    except Exception as e:
        print(f"Error in handle_post_created: {str(e)}")

#------------------------------------------------------------------------------------------------------------------#
