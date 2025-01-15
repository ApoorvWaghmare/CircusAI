import os
from openai import AzureOpenAI
import json
import requests
import random
import string
from pathlib import Path

class Dalle:
    def __init__(self, api_version="2024-05-01-preview", endpoint='https://circusaidalleservice.openai.azure.com/', api_key='0bd39cf3951c49b18243e257dd1eda17'):
        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )

    @staticmethod
    def generate_random_seed(length=8):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(length))

    def generate_image(self, prompt, size="1024x1024", n=1, quality="hd", style="vivid"):
        result = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=n,
            size=size,
            quality=quality,
            style=style
        )
        image_url = json.loads(result.model_dump_json())['data'][0]['url']
        seed = self.generate_random_seed()
        # Download the image file temporarily
        temp_file_path = self.download_image(image_url, seed)
        return temp_file_path


    @staticmethod
    def download_image(url, save_as):
        response = requests.get(url)
        if response.status_code == 200:
            local_path = f"{save_as}.png"
            with open(local_path, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded temporarily: {local_path}")
            Path(local_path).resolve()
            return local_path
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
            return None