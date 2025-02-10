from typing import List

from DocumentProcessor import DocumentProcessor
from VectorStore import VectorStore
from RAGGenerator import RAGGenerator

class RAGPipeline:
    def __init__(self, llm_client, document_paths: List[str]):
        self.processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.generator = RAGGenerator(llm_client)
        self.document_paths = document_paths
    
    def build_index(self):
        docs = self.processor.process_documents(self.document_paths)
        self.vector_store.index_documents(docs)
    
    def query(self, user_query: str):
        context = self.vector_store.retrieve_documents(user_query)
        return self.generator.generate_response(user_query, context)