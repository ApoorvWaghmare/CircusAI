from typing import Dict, Any
from rest_framework.serializers import ModelSerializer
from django.db.models import Q, Case, When, IntegerField
from django.db.models.query import QuerySet
import requests
import random
import json
import time
import os
from PIL import Image
import string

#----------#

from utilities.custom import Service
from apps.user.services import UserQueryService, UserFollowingQueryService, UserBlockQueryService
from apps.aws import cloudfront_service, S3Service
from apps.engagement.services import EngagementQueryService

#----------#

from .models.mysql_models import Post, GenMediaRef, PromptedMediaRef, PostReport, ImageTextRef
from .models.mongo_models import Prompt, Caption, ImageText
from .config import Config
from .signals import post_created
from .dalle import Dalle
from .flux_pro import Flux_pro
from .gemini import Gemini
from .gemini_text import GeminiTextGenerator
from .water_mark_service import WatermarkService

#======================================================================================================================#
# PostQueryService
#======================================================================================================================#

@Service.wrap
class PostQueryService:

    service_type = 'Query'

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_post(pk: int) -> Post:
        return Post.objects.get(pk = pk)
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_home_feed(pk: int) -> QuerySet:
        print('home feed')
        # Fetching followee ids
        user_followee_ids = UserFollowingQueryService.get_user_followee_ids(pk)
        # Filtering blocked followees should be done here
        blocked_user_ids = UserBlockQueryService.get_blocked_user_ids(pk)
        user_followee_ids = UserQueryService.exclude(primary_queryset = user_followee_ids,
                                                     exclude_queryset = blocked_user_ids)
        # Fetching recent posts of all the followees
        posts = Post.objects.filter(user_id__in = user_followee_ids,
                                    post_visibility__in = [Post.Post_Visibility.PUBLIC,
                                                           Post.Post_Visibility.FOLLOWERS_ONLY]).order_by('-creation_timestamp')
        # Get trending posts
        trending_posts = EngagementQueryService.get_most_liked_posts(days = 1)
        # merging posts and trending_posts
        trending_post_ids = list(trending_posts.values_list('post_id', flat = True))
        post_ids = list(posts.values_list('id', flat = True))
        post_ids = trending_post_ids + list(set(post_ids) - set(trending_post_ids))
        preserved_order = Case(*[When(id = pk, then = pos) for pos, pk in enumerate(post_ids)],
                               output_field = IntegerField(),)
        posts = Post.objects.filter(id__in = post_ids).order_by(preserved_order)
        # Fitering reported posts should be done here
        reported_post_ids = PostReport.objects.filter(user_id = pk).values_list('post_id', flat = True)
        posts = posts.exclude(id__in = reported_post_ids)
        return posts
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_search_feed(pk: int) -> QuerySet:
        # Fetch all public posts except posts created by ( user_id = pk )
        public_posts = Post.objects.filter(post_visibility = Post.Post_Visibility.PUBLIC).exclude(user_id = pk).order_by('-creation_timestamp')
        # Filter reported posts here
        reported_post_ids = PostReport.objects.filter(user_id = pk).values_list('post_id', flat = True)
        public_posts = public_posts.exclude(id__in = reported_post_ids)
        # Filter posts by blocked users here
        return public_posts
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_profile_feed(pk: int) -> QuerySet:
        # Fetch user
        user = UserQueryService.get_user(pk)
        return Post.objects.filter(user_id = user, post_visibility = Post.Post_Visibility.PUBLIC).order_by('-creation_timestamp')
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def search_posts(query: str) -> QuerySet:
        # fetch all post_ids which have the query in their captions and prompts
        captions = Caption.objects(__raw__ = { 'caption': {'$regex': query, '$options': 'i'} })
        c_post_ids = set([caption.post_id for caption in captions])
        prompts = Prompt.objects(__raw__ = { 'positive_prompt': {'$regex': query, '$options': 'i'} })
        p_post_ids = set([prompt.post_id for prompt in prompts])
        post_ids = list(c_post_ids.union(p_post_ids))
        # Getting all the posts from the posts_ids that have public visibility
        return Post.objects.filter(id__in = post_ids,
                                   post_visibility = Post.Post_Visibility.PUBLIC).order_by('-creation_timestamp')

#======================================================================================================================#
# End of PostQueryService
#======================================================================================================================#

#======================================================================================================================#
# PostAtomicService
#======================================================================================================================#

@Service.wrap
class PostAtomicService:

    service_type = 'Atomic'

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def update_post_visibiility(post_id: int) -> None:
        post = PostQueryService.get_post(post_id)
        post.post_visibility = Post.Post_Visibility.PUBLIC
        post.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def add_caption(post_id: int, caption: str) -> None:
        post = PostQueryService.get_post(post_id)
        post.caption_ref = Caption.save_caption(caption = caption, post_id = post.id)
        post.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def add_image_text(text: str, text_attributes: dict, post_id: int) -> None:
        post = PostQueryService.get_post(post_id)
        ref = ImageText.save_image_text(text = text, text_attributes = text_attributes, post_id = post.id)
        image_text_ref  = ImageTextRef(post_id = post, image_text_ref = ref)
        image_text_ref.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def save_serializer(serializer: ModelSerializer) -> None:
        serializer.save()

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def delete_post(post_id: int) -> None:
        # delete from mongodb
        Prompt.delete_prompt_by_post_id(post_id = post_id)
        print("deleted from mongodb")
        # get post and gen_media_ref
        post = PostQueryService.get_post(post_id)
        gen_media_ref = GenMediaRef.objects.get(post_id = post)
        # delete from S3
        prompted_media_ref = S3Service().delete(key = gen_media_ref.gen_media_ref)
        print('deleted from S3')
        # delete gen_media_ref
        gen_media_ref.delete()
        print('deleted gen_media_ref')
        # delete post
        post.delete()
        print('deleted post')


#======================================================================================================================#
# End of PostAtomicService
#======================================================================================================================#

#======================================================================================================================#
# CreatePostService
#======================================================================================================================#

class CreatePostService:

    #------------------------------------------------------------------------------------------------------------------#

    def __init__(self):
        self.gemini = Gemini()

    #------------------------------------------------------------------------------------------------------------------#

    def __strip_prompt(prompt: str) -> str:
        return prompt.strip().replace('\n', ' ')
    
    #------------------------------------------------------------------------------------------------------------------#

    def __call_ai_engine(api_json: dict) -> str:
        print(f"Making request to: {Config.COMFYUI_AI_ENGINE_SETTINGS['prompt_api']}")
        print(f"With prompt data: {json.dumps(api_json, indent = 2)}")
        response = requests.post(Config.COMFYUI_AI_ENGINE_SETTINGS['prompt_api'], json = api_json)
        print(f"Request URL: {response.url}")
        print(f"AI engine status code: {response.status_code}")
        # handle response
        prompt_id = None
        try:
            response_data = response.json()
            print("AI engine response:", json.dumps(response_data, indent=2))
            # Process the response data as needed
            prompt_id = response_data.get('prompt_id')
            print('prompt_id:', prompt_id)
        except json.JSONDecodeError:
            print("Failed to decode JSON response")
            print("Response content:", response.text)
            prompt_id = None
        # Poll the AI engine for the generated image
        polling_start_time = time.time()
        gen_media_ref = ''
        if prompt_id != None:
            while True:
                if time.time() - polling_start_time > Config.AI_ENGINE_POLLING_DURATION: 
                    print("Polling duration exceeded")
                    break
                else:
                    response = requests.get(Config.COMFYUI_AI_ENGINE_SETTINGS['queue_history_api'])
                    if response.status_code == 200:
                        response_data = response.json()
                        print("Got Queue history API response but not the image")
                        if (prompt_id in response_data) and (response_data[prompt_id]['status']['completed'] == True):
                            filename = response_data[prompt_id]['outputs']['9']['images'][0]['filename']
                            gen_media_ref = os.path.join(Config.COMFYUI_AI_ENGINE_SETTINGS['output_directory'], filename)
                            print("Output image = ", gen_media_ref)
                            break
                        else:
                            time.sleep(5)
                            continue
                    elif response.status_code == 404:
                        print("Queue history API not found")
                        break
        return gen_media_ref
      
    #------------------------------------------------------------------------------------------------------------------#

    # @staticmethod
    def text_2_image(user_id: int, prompt: str, width: int = 512, height : int = 512) -> Post:
        # prompt = CreatePostService.__strip_prompt(prompt)
        # # Read api_json body from JSON file
        # try:
        #     with open(Config.COMFYUI_AI_ENGINE_SETTINGS['text_2_image_api_body_path'], 'r') as file:
        #         prompt_data = json.load(file)
        # except FileNotFoundError:
        #     print(f"Error: JSON file not found at {Config.COMFYUI_AI_ENGINE_SETTINGS['text_2_image_api_body_path']}")
        #     return None
        # except json.JSONDecodeError:
        #     print(f"Error: Invalid JSON in file {Config.COMFYUI_AI_ENGINE_SETTINGS['text_2_image_api_body_path']}")
        #     return None
        # # Update the prompt and seed in the loaded JSON data
        # prompt_data['6']['inputs']['text'] = prompt
        # prompt_data['31']['inputs']['seed'] = random.randint(Config.COMFYUI_AI_ENGINE_SETTINGS['seed_min'],
        #                                                     Config.COMFYUI_AI_ENGINE_SETTINGS['seed_max'])
        # print('Updated prompt data:', json.dumps(prompt_data, indent = 2))
        # # Prepare the full api_json body
        # api_json = {"prompt": prompt_data}
        # Make the API call
        # gen_media_ref = CreatePostService.__call_ai_engine(api_json = api_json)  
        gen_media_ref = Flux_pro().get_image(prompt, width, height)
        gen_media_ref = WatermarkService.add_watermark(gen_media_ref)
        print("==========================")
        print(gen_media_ref)
        print("==========================")
        # upload the image on cloud here
        gen_media_ref = S3Service().upload(gen_media_ref, delete_local = True)
        # creating a post draft in mysql
        post = Post(user_id = UserQueryService.get_user(user_id))
        post.save()
        # saving media ref for post
        gen_media_ref = GenMediaRef(post_id = post, gen_media_ref = gen_media_ref)
        gen_media_ref.save()
        # saving prompt
        prompt_id = Prompt.save_prompt(positive_prompt = prompt, negative_prompt = '', post_id = post.id)
        # updating mysql post draft
        post.prompt_ref = prompt_id
        post.save()
        # call notification signal
        post_created.send(sender = post, user = UserQueryService.get_user(user_id))
        return post
    
    #------------------------------------------------------------------------------------------------------------------#

    # @staticmethod
    def text_image_2_image(self, user_id: int, prompt: str, ref_post_id: int, width: int = 1024, length : int = 1024) -> Post:
        # prompt = CreatePostService.__strip_prompt(prompt)
        # # Read api_json body from JSON file
        # try:
        #     with open(Config.COMFYUI_AI_ENGINE_SETTINGS['text_image_2_image_api_body_path'], 'r') as file:
        #         prompt_data = json.load(file)
        # except FileNotFoundError:
        #     print(f"Error: JSON file not found at {Config.COMFYUI_AI_ENGINE_SETTINGS['text_image_2_image_api_body_path']}")
        #     return None
        # except json.JSONDecodeError:
        #     print(f"Error: Invalid JSON in file {Config.COMFYUI_AI_ENGINE_SETTINGS['text_image_2_image_api_body_path']}")
        #     return None
        # # get ref_post
        # post = PostQueryService.get_post(ref_post_id)
        # # download image from S3
        # prompted_media_ref = GenMediaRef.objects.get(post_id = post).gen_media_ref
        # print("prompted_media_ref = ", prompted_media_ref)
        # prompted_media_ref = S3Service().download(prompted_media_ref)
        # # Update the prompt and seed in the loaded JSON data
        # prompt_data['3']['inputs']['seed'] = random.randint(Config.COMFYUI_AI_ENGINE_SETTINGS['seed_min'],
        #                                                     Config.COMFYUI_AI_ENGINE_SETTINGS['seed_max'])
        # prompt_data['6']['inputs']['text'] = prompt
        # prompt_data['10']['inputs']['image'] = prompted_media_ref
        # print('Updated prompt data:', json.dumps(prompt_data, indent = 2))        
        # # Prepare the full api_json body
        # api_json = {"prompt": prompt_data}
        # # Make the API call
        # gen_media_ref = CreatePostService.__call_ai_engine(api_json = api_json)  
        # # upload the image on cloud here
        # gen_media_ref = S3Service().upload(gen_media_ref)
        # # creating a post draft in mysql
        # post = Post(user_id = UserQueryService.get_user(user_id))
        # post.save()
        # # saving media ref for post
        # gen_media_ref = GenMediaRef(post_id = post, gen_media_ref = gen_media_ref)
        # gen_media_ref.save()
        # # saving prompt
        # prompt_id = Prompt.save_prompt(positive_prompt = prompt, negative_prompt = '', post_id = post.id)
        # # updating mysql post draft
        # post.prompt_ref = prompt_id
        # post.save()
        # # call notification signal
        # post_created.send(sender = post, user = UserQueryService.get_user(user_id))
        # return post


        # get ref_post
        post = PostQueryService.get_post(ref_post_id)
        # download image from S3
        prompted_media_ref = GenMediaRef.objects.get(post_id = post).gen_media_ref
        print("prompted_media_ref = ", prompted_media_ref)
        prompted_media_ref = S3Service().download(prompted_media_ref)
        # get image text from gemini
        image_text =  self.gemini.image2text(image_ref = prompted_media_ref)
        os.remove(prompted_media_ref)
        gen_media_ref = Flux_pro().get_image(image_text + " " + prompt, width, length)
        gen_media_ref = WatermarkService.add_watermark(gen_media_ref)
        print("==========================")
        print(gen_media_ref)
        print("==========================")
        # upload the image on cloud here
        gen_media_ref = S3Service().upload(gen_media_ref, delete_local = True)
        # creating a post draft in mysql
        post = Post(user_id = UserQueryService.get_user(user_id))
        post.save()
        # saving media ref for post
        gen_media_ref = GenMediaRef(post_id = post, gen_media_ref = gen_media_ref)
        gen_media_ref.save()
        # saving prompt
        prompt_id = Prompt.save_prompt(positive_prompt = prompt, negative_prompt = '', post_id = post.id)
        # updating mysql post draft
        post.prompt_ref = prompt_id
        post.save()
        # call notification signal
        post_created.send(sender = post, user = UserQueryService.get_user(user_id))
        return post

#------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def text_face_2_image(user_id: int, prompt: str, face_image_file: object) -> Post:
        prompt = CreatePostService.__strip_prompt(prompt)
        # Read api_json body from JSON file
        try:
            with open(Config.COMFYUI_AI_ENGINE_SETTINGS['text_face_2_image_api_body_path'], 'r') as file:
                prompt_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: JSON file not found at {Config.COMFYUI_AI_ENGINE_SETTINGS['text_face_2_image_api_body_path']}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file {Config.COMFYUI_AI_ENGINE_SETTINGS['text_face_2_image_api_body_path']}")
            return None
        # get face image to
        face_image = Image.open(face_image_file)
        prompted_media_ref = Config.COMFYUI_AI_ENGINE_SETTINGS['input_directory'] + '/face_image' + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))+ str(time.time()) + '.png'
        face_image.save(prompted_media_ref)
        # Update the prompt and seed in the loaded JSON data
        prompt_data['3']['inputs']['seed'] = random.randint(Config.COMFYUI_AI_ENGINE_SETTINGS['seed_min'],
                                                                             Config.COMFYUI_AI_ENGINE_SETTINGS['seed_max'])
        prompt_data['6']['inputs']['text'] = prompt
        prompt_data['10']['inputs']['image'] = prompted_media_ref
        print('Updated prompt data:', json.dumps(prompt_data, indent = 2))        
        # Prepare the full api_json body
        api_json = {"prompt": prompt_data}
        # Make the API call
        gen_media_ref = CreatePostService.__call_ai_engine(api_json = api_json)  
        # upload the prompted media and gen_media_ref image on cloud here
        gen_media_ref = S3Service().upload(gen_media_ref)
        prompted_media_ref = S3Service().upload(prompted_media_ref)
        # creating a post draft in mysql
        post = Post(user_id = UserQueryService.get_user(user_id))
        post.save()
        # saving media ref for post
        gen_media_ref = GenMediaRef(post_id = post, gen_media_ref = gen_media_ref)
        gen_media_ref.save()
        prompted_media_ref = PromptedMediaRef(post_id = post, prompted_media_ref = prompted_media_ref)
        prompted_media_ref.save()
        # saving prompt
        prompt_id = Prompt.save_prompt(positive_prompt = prompt, negative_prompt = '', post_id = post.id)
        # updating mysql post draft
        post.prompt_ref = prompt_id
        post.save()
        # call notification signal
        post_created.send(sender = post, user = UserQueryService.get_user(user_id))
        return post

#------------------------------------------------------------------------------------------------------------------#
    
    @staticmethod
    def upload_image(image_file:object):
        image = Image.open(image_file)
        prompted_media_ref = Config.COMFYUI_AI_ENGINE_SETTINGS['input_directory'] + '/image' + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))+ str(time.time()) + '.png'
        image.save(prompted_media_ref)
        gen_media_ref = S3Service().upload(gen_media_ref, delete_local=True)
        return gen_media_ref
#======================================================================================================================#
# End of CreatePostService
#======================================================================================================================#

#======================================================================================================================#
# PostReportService
#======================================================================================================================#

@Service.wrap
class PostReportService:

    service_type = 'Atomic'

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def report_post(data: Dict[str, Any]) -> None:
        report = PostReport(post_id = PostQueryService.get_post(data.pop('post_id')), 
                            user_id = UserQueryService.get_user(data.pop('user_id')), 
                            report = data.pop('report'), 
                            user_report = data.pop('user_report'))
        report.save()

#======================================================================================================================#
# End of PostReportService
#======================================================================================================================#

#======================================================================================================================#
# RandomAnimePromptService
#======================================================================================================================#

@Service.wrap
class GeminiTextGeneratorService:
    """ A service class that interacts with the GeminiTextGenerator """
    service_type = 'Query'
    
    @staticmethod
    def generate_anime_prompt():
        """ Use the imported GeminiTextGenerator to generate an anime-style image prompt """
        # Instantiate the GeminiTextGenerator from gemini_text.py
        generator = GeminiTextGenerator()

        # Generate the anime-style prompt using the generator
        return generator.generate_anime_prompt()

#======================================================================================================================#
# End of RandomAnimePromptService
#======================================================================================================================#
