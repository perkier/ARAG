import requests

from google import genai

from Base_Client import LLMClient

class GeminiClient(LLMClient):
    """
    Gemini API Client
    """
    BASE_URL = "https://api.google.com/gemini/v1/generate"

    def __init__(self):
        
        self.service_name: str = "Gemini"

        super().__init__(self.service_name)

        self.client = genai.Client(api_key=self.password)

    def generate_text(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents = prompt,
        )
        return response.text
