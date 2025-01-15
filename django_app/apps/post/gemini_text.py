import google.generativeai as genai
import os

os.environ['GEMINI_API_KEY'] = "AIzaSyCsyxCsUZN1klnYWp0F0jTgCGJWI108qxA"

class GeminiTextGenerator:
    
    def __init__(self, api_key=None, model_type="gemini-1.5-flash"):
        """ Initialize the GeminiTextGenerator class with the API key and model type """
        # Load API key from environment if not provided
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("API key is required. Please provide it directly or set it as the 'GEMINI_API_KEY' environment variable.")
        
        # Configure the Generative AI API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(model_type)
    
    def generate_anime_prompt(self):
        """ Generate a random prompt for creating an anime-style image """
        # The text prompt to generate an anime-style image description
        prompt = ("Generate a random prompt for creating an anime-style image that is either very cute or highly engaging. "
                  "Provide detailed descriptions of characters, environment, and mood. The scene should feel dynamic, with "
                  "a mix of fantasy or action elements, and the characters should have distinctive traits typical of anime "
                  "(e.g., large expressive eyes, vibrant hair colors, exaggerated emotions). Ensure the setting is vibrant "
                  "and colorful, either enhancing the cuteness or creating an intense, captivating atmosphere. Limit it to 100 words.")
        
        # Generate the content using the model
        response = self.model.generate_content(prompt)
        
        # Return the generated text
        return response.text


# Example usage
if __name__ == "__main__":
    # Instantiate the class (assuming the API key is set in the environment)
    generator = GeminiTextGenerator()

    # Generate the anime-style image prompt
    result = generator.generate_anime_prompt()
    
    # Print the generated prompt
    print(result)
