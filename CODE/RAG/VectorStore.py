import os
from typing import List
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

class VectorStore:
    def __init__(self, embedding_model: str = "text-embedding-ada-002"):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = None
    
    def index_documents(self, documents: List[Document]):
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
    
    def retrieve_documents(self, query: str, k: int = 3) -> List[str]:
        if not self.vector_store:
            raise ValueError("Vector store is empty. Index documents first.")
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]