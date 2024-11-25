import vertexai
from vertexai.generative_models import GenerativeModel, Image, Part, Content
import vertexai.preview.generative_models as generative_models
import json
import random
import time

class GeminiModel:
    def __init__(self, json_mode=False):
        vertexai.init(project="cd-ds-384118", location="us-south1")
        self.model = GenerativeModel(model_name="gemini-1.5-pro-001")

        self.generation_config = {
            "max_output_tokens": 8192,
            "temperature": 0.2,
            "top_p": 0.95,
            "response_mime_type": "application/json" if json_mode else "text/plain",
        }

        self.safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
        }

    def generate_response(
        self, content: Content
    ):
        """
        Generates a response based on the provided prompt or function response.

        Args:
            prompt (Optional[str]): A text prompt to generate a response. If None, function_response must be provided.
            function_response (Optional[dict]): A dictionary representing the response from a function call. If None, prompt must be provided.

        Returns:
            Union[dict, str]: The generated response, which could be a function call (dict) or plain text (str).

        Raises:
            ValueError: If neither a prompt nor a function_response is provided.
        """

        response = self.chat.send_message(
            content,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            stream=False,
        )
        time.sleep(30) # Rate limiting based on our token limit
        function_calls = response.candidates[0].function_calls

        if len(function_calls) > 0:
            return function_calls

        return response.text
    
    def extract_text_from_img(self, im_bytes, prompt):
        # Load image
        image_part = Part.from_data(
            im_bytes.getvalue(),
            mime_type='image/jpeg'
        )

        #provide image and prompt to extract text
        response = self.model.generate_content(
            [image_part, prompt]
            )
        return response.text

    def image_to_text_gemini(self, image):


        prompt = '''
        Extract all visible text from the image and output a string
        '''
        try:
            result = self.extract_text_from_img(image, prompt)
        except:
            result = ''
        return result