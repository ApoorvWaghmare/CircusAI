from rest_framework.serializers import ModelSerializer, SerializerMethodField

#----------#

from apps.user.serializers import UserCommentSerializer

#----------#

from .models import mysql_models, mongo_models

#======================================================================================================================#
# SaveCommentSerializer
#======================================================================================================================#

class SaveCommentSerializer(ModelSerializer):
    
    class Meta:
        model = mysql_models.Comment
        fields = ['post_id', 'comment']

#======================================================================================================================#
# End of SaveCommentSerializer
#======================================================================================================================#

#======================================================================================================================#
# GetAllCommentsSerializer
#======================================================================================================================#

class GetAllCommentsSerializer(ModelSerializer):

    #------------------------------------------------------------------------------------------------------------------#

    comment_ref = SerializerMethodField()
    user = UserCommentSerializer(read_only = True, source = 'user_id')

    #------------------------------------------------------------------------------------------------------------------#
    
    class Meta:
        model = mysql_models.Comment
        fields = ['post_id', 'timestamp', 'comment_ref', 'user']

    #------------------------------------------------------------------------------------------------------------------#
        
    def get_comment_ref(self, obj):
        try:
            comment_id = obj.comment_ref
            document = mongo_models.Comment.objects.get(id = comment_id)
            comment = document.comment
            return comment
        except Exception as e:
            print(e)
            return None


#======================================================================================================================#
# End of GetAllCommentsSerializer
#======================================================================================================================#
