import ollama

from Base_Client import LLMClient

class LlamaClient(LLMClient):
    """
    Llama API Client
    """

    def __init__(self):
        
        self.service_name: str = "llama3.2"

        super().__init__(self.service_name)

        self.client = ollama.Client()
        self.client.pull("llama3.2")

    def generate_text(self, prompt: str) -> str:

        response = self.client.generate(
            model=self.service_name,
            prompt = prompt,
        )

        return response["response"]
