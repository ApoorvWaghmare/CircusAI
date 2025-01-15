from rest_framework.serializers import ModelSerializer, SerializerMethodField
import json

#----------#

from .models import Notification

#======================================================================================================================#
# NotificationSerializer
#======================================================================================================================#

class NotificationSerializer(ModelSerializer):

    message_attributes = SerializerMethodField()

    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        model = Notification
        fields = ['subject', 'message', 'message_attributes', 'timestamp']
    
    #------------------------------------------------------------------------------------------------------------------#

    def get_message_attributes(self, obj):
        try:
            return json.loads(obj.message_attributes)
        except:
            print('Failed to convert notification message attributes json')
            return obj.message_attributes

#======================================================================================================================#
# End of NotificationSerializer
#======================================================================================================================#

