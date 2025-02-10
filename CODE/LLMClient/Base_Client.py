import requests
import configparser
import os
from abc import ABC, abstractmethod

# Load API keys from config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../cfg/api_keys.cfg")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

class LLMClient(ABC):
    """
    Abstract base class for LLM API clients.
    """
    def __init__(self, service_name: str):

        self.service_name: str = service_name

        self.keys = self.get_api_key()

        if not self.keys:
            raise ValueError("API key is required")

    def get_api_key(self) -> str:
        return config.get("API_KEYS", self.service_name, fallback=None)

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Generates text based on the given prompt."""
        pass
