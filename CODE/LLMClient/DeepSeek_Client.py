import requests

from openai import OpenAI

from Base_Client import LLMClient

class DeepSeekClient(LLMClient):
    """
    DeepSeek API Client
    """
    BASE_URL = "https://api.deepseek.com/v1/generate"

    def __init__(self):

        self.service_name: str = "DeepSeek"

        super().__init__(self.service_name)

        self.client = OpenAI(api_key=self.password, base_url="https://api.deepseek.com")

    def generate_text(self, prompt: str) -> str:
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},
            ],
            stream=False
        )

        return response.choices[0].message.content