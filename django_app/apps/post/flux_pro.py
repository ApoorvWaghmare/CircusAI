import fal_client
import requests
import string
import random
import time
import os

os.environ['FAL_KEY'] = "a1c072e6-b93f-41cb-9dcf-d1714a63e95d:a0cf235103dd6df436b3a77d373f9db6"

class Flux_pro:

    def __on_queue_update(self, update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(log["message"])

    def get_image(self, prompt: str, width: int = 512, height : int = 512) -> str:
        result = fal_client.subscribe(
            "fal-ai/flux-pro/v1.1",
            arguments={
                "prompt": prompt,
                "image_size": {
                    "width": width,
                    "height": height
                },
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1,
                "safety_tolerance": "5",
                "prompt_upsampling": False,
            },
            with_logs = True,
            on_queue_update = self.__on_queue_update,
        )
        print("Results:", result)
        image_url = result["images"][0]["url"]
        response = requests.get(image_url)
        image_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))+ str(time.time()) + ".png"
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open a file in binary mode and write the content of the image to it
            with open(image_url, "wb") as f:
                f.write(response.content)
            print("Image downloaded successfully!")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
        return image_url
