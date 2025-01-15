from mongoengine import Document, StringField, IntField, DictField, ListField
from bson import ObjectId

#----------#

#======================================================================================================================#
# Caption
#======================================================================================================================#

class Caption(Document):

    #------------------------------------------------------------------------------------------------------------------#

    caption = StringField()
    post_id = IntField(required = True, unique = True)

    meta = {
        'collection': 'captions',  # Collection name in MongoDB
        'indexes': [
            'caption',  # Index on the 'component' field to optimize queries
            'post_id',
        ]
    }

    #------------------------------------------------------------------------------------------------------------------#

    @classmethod
    def save_caption(cls, caption, post_id):
        try:
            caption = cls(caption = caption, post_id = post_id)
            print(caption.save())
            return str(caption.id)
        except Exception as e:
            print(e)
            return None

#======================================================================================================================#
# End of Caption
#======================================================================================================================#

#======================================================================================================================#
# Prompt
#======================================================================================================================#

class Prompt(Document):

    #------------------------------------------------------------------------------------------------------------------#

    positive_prompt = StringField()
    negative_prompt = StringField()
    post_id = IntField(required = True, unique = True)

    meta = {
        'collection': 'prompts',  # Collection name in MongoDB
        'indexes': [
            'positive_prompt',  # Index on the 'component' field to optimize queries
            'negative_prompt',
            'post_id',
        ]
    }

    #------------------------------------------------------------------------------------------------------------------#

    @classmethod
    def save_prompt(cls, positive_prompt: str, negative_prompt: str, post_id: int):
        try:
            prompt = cls(positive_prompt = positive_prompt, negative_prompt = negative_prompt, post_id = post_id)
            print(prompt.save())
            return str(prompt.id)
        except Exception as e:
            print(e)
            return None
        
    #------------------------------------------------------------------------------------------------------------------#
        
    @classmethod
    def delete_prompt_by_post_id(cls, post_id: int) -> bool:
        try:
            prompt = cls.objects(post_id=post_id).first()
            if prompt:
                prompt.delete()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

#======================================================================================================================#
# End of Prompt
#======================================================================================================================#

#======================================================================================================================#
# ImageText
#======================================================================================================================#

class ImageText(Document):

    #------------------------------------------------------------------------------------------------------------------#

    text = StringField()
    text_attributes = DictField()
    post_id = IntField(required = True)

    meta = {
        'collection': 'image_texts',  # Collection name in MongoDB
        'indexes': [
            'text',  # Index on the 'component' field to optimize queries
            'post_id',
        ]
    }

    #------------------------------------------------------------------------------------------------------------------#

    @classmethod
    def save_image_text(cls, text, text_attributes, post_id):
        try:
            image_text = cls(text = text, text_attributes = text_attributes, post_id = post_id)
            print(image_text.save())
            return str(image_text.id)
        except Exception as e:
            print(e)
            return None

#======================================================================================================================#
# End of ImageText
#======================================================================================================================#

#======================================================================================================================#
# MediaTags
#======================================================================================================================#

class MediaTags(Document):

    #------------------------------------------------------------------------------------------------------------------#

    media_ref = StringField(required = True, unique = True)
    tags = DictField(default = {"genre": ListField(StringField()),
                                "subject": ListField(StringField()),
                                "mood": ListField(StringField()),
                                "color": ListField(StringField()),
                                "style": ListField(StringField()),
                                "theme": ListField(StringField()),
                                "composition": ListField(StringField()),
                                "location": ListField(StringField()),
                                "medium": ListField(StringField())})

    meta = {
        'collection': 'image_tags',  # Collection name in MongoDB
        'indexes': [
            'media_ref',  # Index on media_ref field for faster queries
            {
                'fields': ['$tags.genre', '$tags.subject', '$tags.mood', '$tags.color', 
                           '$tags.style', '$tags.theme', '$tags.composition', 
                           '$tags.location', '$tags.medium'],
                'default_language': 'english',
                'weights': {'tags.genre': 10, 'tags.subject': 10, 'tags.mood': 5, 
                            'tags.color': 5, 'tags.style': 7, 'tags.theme': 8, 
                            'tags.composition': 6, 'tags.location': 4, 'tags.medium': 3}
            }
        ]
    }

    #------------------------------------------------------------------------------------------------------------------#

    @classmethod
    def save_media_tags(cls, 
                        media_ref: str, 
                        genre: list, 
                        subject: list, 
                        mood: list, 
                        color: list, 
                        style: list, 
                        theme: list, 
                        composition: list, 
                        location: list, 
                        medium: list):
        tags = {"genre": genre, 
                "subject": subject, 
                "mood": mood, 
                "color": color, 
                "style": style,
                "theme": theme,
                "composition": composition,
                "location": location,
                "medium": medium}
        return cls(media_ref = media_ref, tags = tags).save()
    
    #------------------------------------------------------------------------------------------------------------------#

    @classmethod
    def find_by_media_ref(cls, media_ref):
        return cls.objects(media_ref = media_ref).first()
    
    #------------------------------------------------------------------------------------------------------------------#

    @classmethod
    def find_by_tags(cls, tags, match_all = False):
        query = {}
        for key, value in tags.items():
            if match_all:
                query[f"tags.{key}__all"] = value
            else:
                query[f"tags.{key}__in"] = value
        return cls.objects(**query)

#======================================================================================================================#
# End of MediaTags
#======================================================================================================================#