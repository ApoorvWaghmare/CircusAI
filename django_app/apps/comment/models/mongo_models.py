from mongoengine import Document, StringField, IntField
from bson import ObjectId

#----------#

#======================================================================================================================#
# Comment
#======================================================================================================================#

class Comment(Document):

    #------------------------------------------------------------------------------------------------------------------#

    comment = StringField(required = True)
    user_id = IntField(required = True)
    post_id = IntField(required = True)

    meta = {
        'collection': 'comments',  # Collection name in MongoDB
        'indexes': [
            'user_id',  # Index on the 'component' field to optimize queries
            'post_id',
        ]
    }

    #------------------------------------------------------------------------------------------------------------------#

    @classmethod
    def save_comment(cls, comment, user_id, post_id):
        try:
            comment = cls(comment = comment, user_id = user_id, post_id = post_id)
            print(comment.save())
            return str(comment.id)
        except Exception as e:
            print(e)
            return None

#======================================================================================================================#
# End of Comment
#======================================================================================================================#