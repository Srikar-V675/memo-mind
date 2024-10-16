# Documentation

This document provides a detailed overview of the Memo-Mind project, including its architecture, features, and future plans. Memo-Mind is a personalized Retrieval-Augmented Generation (RAG) chatbot built using Qdrant and LangChain, designed to serve as a personal knowledge assistant. Unlike generic chatbots, Memo-Mind is tailored to your unique knowledge base, focusing on your personal notes and writing style. The chatbot does not work with sensitive personal data like credit cards or financial information; instead, it leverages your self-curated content such as notes, social media interactions, and code repositories to provide context-aware assistance.

## Architecture

```mermaid
flowchart TD
    %% Data Ingestion and Preprocessing
    A[User Data Sources] --> |Obsidian Notes, Markdown Files| B[Data Ingestion]
    B --> C[Text Chunking and Preprocessing]
    C --> D[Embedding Generation]
    
    %% Embedding and Vector Store
    D --> E[HuggingFace Embeddings Model]
    E --> F[Qdrant Vector Store]
    
    %% Retrieval
    F --> G[Document Retriever]
    
    %% LLM Processing
    G --> |Retrieved Context| H[Custom Prompt Template]
    H --> I[Generative AI Model]
    I --> J[Response Generation]
    
    %% User Interface
    J --> K[Streamlit Frontend]
    
    %% Feedback Loop
    K --> |User Feedback| L[Prompt Refinement]
    L --> H

    %% Labels for clarity
    subgraph Data Preparation
        B
        C
        D
        E
    end
    
    subgraph Retrieval Augmented Generation RAG
        F
        G
        H
        I
        J
    end
    
    subgraph User Interaction
        K
        L
    end
```
