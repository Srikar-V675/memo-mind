import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Assuming you already have the embedding and vector store functions defined

class NotesHandler(FileSystemEventHandler):
    def __init__(self, vector_store, embeddings):
        self.vector_store = vector_store
        self.embeddings = embeddings

    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            print(f'Modified: {event.src_path}')
            self.process_file(event.src_path)

    def on_created(self, event):
        if event.src_path.endswith('.md'):
            print(f'Created: {event.src_path}')
            self.process_file(event.src_path)

    def process_file(self, file_path):
        # Read and process the markdown file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Split the content into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(content)
        
        # Embed the chunks
        embeddings = self.embeddings.embed_documents(chunks)
        
        # Store the embeddings in the vector store
        for chunk, embedding in zip(chunks, embeddings):
            self.vector_store.add_texts(texts=[chunk], embeddings=[embedding])

def main():
    notes_directory = 'path/to/your/notes'  # Specify your notes directory
    embeddings = OpenAIEmbeddings()  # Initialize your embeddings
    vector_store = FAISS()  # Initialize your FAISS vector store

    event_handler = NotesHandler(vector_store, embeddings)
    observer = Observer()
    observer.schedule(event_handler, path=notes_directory, recursive=False)

    observer.start()
    print("Monitoring changes in the notes directory...")

    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
