from mongoengine import Document, StringField, IntField
from bson import ObjectId
from mongoengine.errors import NotUniqueError, ValidationError

#----------#

#======================================================================================================================#
# Bio
#======================================================================================================================#

class Bio(Document):

    #------------------------------------------------------------------------------------------------------------------#

    bio = StringField(required = True)
    user_id = IntField(required = True, unique = True)

    meta = {
        'collection': 'bios',  # Collection name in MongoDB
        'indexes': [
            'bio',  # Index on the 'component' field to optimize queries
            'user_id',
        ]
    }

    #------------------------------------------------------------------------------------------------------------------#

    @classmethod
    def save_bio(cls, bio, user_id):
        try:
            # Try to find an existing document with the given user_id
            existing_bio = cls.objects(user_id=user_id).first()
            
            if existing_bio:
                # If a document exists, update it
                existing_bio.bio = bio
                existing_bio.save()
                return str(existing_bio.id)
            else:
                # If no document exists, create a new one
                new_bio = cls(bio=bio, user_id=user_id)
                new_bio.save()
                return str(new_bio.id)
        
        except NotUniqueError as e:
            print(f"Duplicate user_id error: {e}")
            return None
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

#======================================================================================================================#
# End of Bio
#======================================================================================================================#