import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.schema import Document

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    def process_documents(self, file_paths: List[str]) -> List[Document]:
        documents = []
        for path in file_paths:
            loader = TextLoader(path)
            docs = loader.load()
            documents.extend(self.text_splitter.split_documents(docs))
        return documents