import os
import json
from uuid import uuid4
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
from langchain_core.documents import Document

class DocumentProcessor:
    def __init__(self) -> None:
        self.embedding_model_name = 'BAAI/bge-large-en'
        self.embedding_model = HuggingFaceBgeEmbeddings(model_name=self.embedding_model_name)
        self.qdrant_url = "http://localhost:6333"
        self.client = QdrantClient(url=self.qdrant_url)
        self.collection_name = "vector_db"
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )
        
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embedding_model
        )
    
    def chunk_content(self, content, chunk_size=1000, chunk_overlap=150):
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        # splitter = MarkdownTextSplitter()
        return splitter.split_text(content)
    
    def process_docs(self, documents):
        # Process each document for embedding and storage
        for doc in documents:
            chunked_docs = self.chunk_content(doc['content'])
    
            # Create Document objects for each chunk and assign a unique ID
            document_objects = [
                Document(
                    page_content=chunk, 
                    metadata={
                        "related_notes": doc['related_notes'], 
                        "references": doc['references']}
                    ) for chunk in chunked_docs]
            uuids = [str(uuid4()) for _ in range(len(document_objects))]
    
            # Add documents to the vector store
            self.vector_store.add_documents(documents=document_objects, ids=uuids)

notes_path = 'processed_notes.json'
with open(notes_path, 'r') as f:
    notes = json.load(f)

processor = DocumentProcessor()
processor.process_docs(notes)

print("Documents processed and stored in Qdrant successfully!")
