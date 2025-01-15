from rest_framework.serializers import ModelSerializer, SerializerMethodField

#----------#

from apps.aws.services import CloudfrontService
from apps.user.services import UserQueryService

#----------#

from .models.mysql_models import Post, GenMediaRef, ImageTextRef
from .models.mongo_models import Caption, Prompt, ImageText


#======================================================================================================================#
# GenMediaRefSerializer
#======================================================================================================================#

class GenMediaRefSerializer(ModelSerializer):

    #------------------------------------------------------------------------------------------------------------------#

    gen_media_ref = SerializerMethodField()

    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        model = GenMediaRef
        fields = '__all__'

    #------------------------------------------------------------------------------------------------------------------#
        
    def get_gen_media_ref(self, obj):
        try:
            return CloudfrontService().create_signed_url(s3_object_key = obj.gen_media_ref)
        except Exception as e:
            print(e)
            return None

#======================================================================================================================#
# End of GenMediaRefSerializer
#======================================================================================================================#

#======================================================================================================================#
# ImageTextRefSerializer
#======================================================================================================================#

class ImageTextRefSerializer(ModelSerializer):

    #------------------------------------------------------------------------------------------------------------------#

    image_text_ref = SerializerMethodField()

    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        model = ImageTextRef
        fields = '__all__'

    #------------------------------------------------------------------------------------------------------------------#

    def get_image_text_ref(self, obj):
        try:
            if obj.image_text_ref:
                image_text = ImageText.objects.get(id = obj.image_text_ref)
                image_text = image_text.to_mongo()
                # Use to_dict() to convert to a Python dictionary
                image_text = image_text.to_dict()
                image_text.pop('_id')
                return image_text
            else:
                return []
        except Exception as e:
            print(e)
            return []

#======================================================================================================================#
# End of ImageTextRefSerializer
#======================================================================================================================#

#======================================================================================================================#
# PostSerializer
#======================================================================================================================#

class PostSerializer(ModelSerializer):

    #------------------------------------------------------------------------------------------------------------------#
    
    gen_media_refs = GenMediaRefSerializer(many = True, read_only = True, source = 'gen_media_ref')
    image_text_refs = ImageTextRefSerializer(many = True, read_only = True, source = 'image_text_ref')
    username = SerializerMethodField()
    caption_ref = SerializerMethodField()
    prompt_ref = SerializerMethodField()

    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        model = Post
        fields = '__all__'

    #------------------------------------------------------------------------------------------------------------------#

    def get_username(self, obj):
        try:
            return UserQueryService.get_username(obj.user_id.id)
        except Exception as e:
            print(e)
            return None
        
    #------------------------------------------------------------------------------------------------------------------#

    def get_caption_ref(self, obj):
        try:
            if obj.caption_ref:
                document = Caption.objects.get(id = obj.caption_ref)
                return document.caption
            else:
                return ''
        except Exception as e:
            print(e)
            return ''
    
    #------------------------------------------------------------------------------------------------------------------#

    def get_prompt_ref(self, obj):
        try:
            if obj.prompt_ref:
                document = Prompt.objects.get(id = obj.prompt_ref)
                return document.positive_prompt
            else:
                return ''
        except Exception as e:
            print(e)
            return ''


#======================================================================================================================#
# End of PostSerializer
#======================================================================================================================#

#======================================================================================================================#
# SearchPostsSerializer
#======================================================================================================================#

class SearchPostsSerializer(ModelSerializer):

    #------------------------------------------------------------------------------------------------------------------#

    gen_media_refs = GenMediaRefSerializer(many = True, read_only = True, source = 'gen_media_ref')
    image_text_refs = ImageTextRefSerializer(many = True, read_only = True, source = 'image_text_ref')
    caption_ref = SerializerMethodField()

    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        model = Post
        fields = ['id', 'caption_ref', 'gen_media_refs', 'image_text_refs']

    #------------------------------------------------------------------------------------------------------------------#

    def get_caption_ref(self, obj):
        try:
            if obj.caption_ref:
                document = Caption.objects.get(id = obj.caption_ref)
                return document.caption
            else:
                return ''
        except Exception as e:
            print(e)
            return ''

#======================================================================================================================#
# End of SearchPostsSerializer
#======================================================================================================================#
