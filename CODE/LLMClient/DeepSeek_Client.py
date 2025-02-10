import requests

from Base_Client import LLMClient

class DeepSeekClient(LLMClient):
    """
    DeepSeek API Client
    """
    BASE_URL = "https://api.deepseek.com/v1/generate"

    def __init__(self):

        self.service_name: str = "DeepSeek"

        super().__init__(self.service_name)

    def generate_text(self, prompt: str) -> str:
        response = requests.post(
            self.BASE_URL,
            headers={"Authorization": f"Bearer {self.password}"},
            json={"prompt": prompt}
        )
        return response.json().get("text", "Error: No response")