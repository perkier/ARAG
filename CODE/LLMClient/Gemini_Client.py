import requests

from Base_Client import LLMClient

class GeminiClient(LLMClient):
    """
    Gemini API Client
    """
    BASE_URL = "https://api.google.com/gemini/v1/generate"

    def __init__(self):
        
        self.service_name: str = "Gemini"

        super().__init__(self.service_name)

    def generate_text(self, prompt: str) -> str:
        response = requests.post(
            self.BASE_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"prompt": prompt}
        )
        return response.json().get("text", "Error: No response")
