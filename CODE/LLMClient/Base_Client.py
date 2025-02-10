import json
import os
from abc import ABC, abstractmethod

class LLMClient(ABC):
    """
    Abstract base class for LLM API clients.
    """
    def __init__(self, service_name: str):

        self.service_name: str = service_name

        self.get_api_key()

        #if not self.keys:
        #    raise ValueError("API key is required")

    def get_api_key(self) -> str:

        # Set the path to your DeepSeek.json file
        file_path = os.path.join('..', 'cfg', f'{self.service_name}.json')

        # Initialize username and password as empty strings
        self.username = ''
        self.password = ''

        # Check if the file exists before opening it
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                config = json.load(f)
                self.username = config.get("username", '')
                self.password = config.get("password", '')
        
        return self.username, self.password

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Generates text based on the given prompt."""
        pass
