import google.generativeai as genai
import os
import PIL.Image

class Gemini():

    def __init__(self, key="AIzaSyCsyxCsUZN1klnYWp0F0jTgCGJWI108qxA", model_type = "gemini-1.5-flash"):
        """ Initialize the Gemini class with the API key and model type """

        genai.configure(api_key = key)
        self.model = genai.GenerativeModel(model_type)

    def image2text(self, image_ref, prompt = "Generate a text prompt for this image."):
        """ Generate text based on the image and prompt """
        print(image_ref)
        image = PIL.Image.open(image_ref)
        print("Generating Image text")
        response = self.model.generate_content([prompt, image])
        return response.text
