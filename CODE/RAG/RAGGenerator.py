import os
from typing import List
from langchain.chat_models import ChatOpenAI

class RAGGenerator:
    def __init__(self, llm_client, temperature: float = 0.7):
        self.llm = llm_client
    
    def generate_response(self, query: str, context: List[str]) -> str:
        prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {query}"
        return self.llm.predict(prompt)