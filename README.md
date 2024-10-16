# Memo-Mind

`Memo-Mind` is a personalized Retrieval-Augmented Generation (RAG) chatbot built using Qdrant and LangChain, designed to serve as a personal knowledge assistant. Unlike generic chatbots, Memo-Mind is tailored to your unique knowledge base, focusing on your personal notes and writing style. The chatbot does not work with sensitive personal data like credit cards or financial information; instead, it leverages your self-curated content such as notes, social media interactions, and code repositories to provide context-aware assistance.

Refer to the documentation for more technical details: [[documentation.md |  Documentation]]

## What's Special About Memo-Mind?

While there are many RAG-based chatbots on the internet, Memo-Mind stands out for its personalization capabilities:
- **Built on Your Own Knowledge Base**: Memo-Mind uses your personal notes, social media activity (LinkedIn posts, GitHub code, etc.), and other self-curated content to generate responses. This makes the chatbot's output more aligned with your thinking patterns, preferences, and knowledge.
- **Local and Secure Data Processing**: Initially, Memo-Mind is built on notes from your Obsidian Vault. Obsidian is a powerful markdown-based note-taking tool that allows for local, offline note management with rich linking capabilities via wikilinks. This means your data stays on your machine, ensuring privacy and security.
- **Mimics Your Writing Style**: By analyzing the content you have already written, Memo-Mind adapts to your writing style and tone, providing responses that feel more authentic and personalized.

## Idea

The core vision behind Memo-Mind is to create a digital twin of the user. This "digital twin" is not just a chatbot but a reflection of the user's knowledge, practices, and style. It aims to replicate how you think, write, and solve problems based on your accumulated knowledge base, which includes:
1. **Your Notes**: The primary source of information is your personal notes stored in your Obsidian Vault. These notes can include study materials, thoughts, research, or even casual reflections. Memo-Mind uses these markdown files to build a knowledge graph with meaningful connections and context-aware search capabilities.
2. **Code Practices**: By integrating with code repositories like GitHub, Memo-Mind can understand your coding habits, common practices, and the types of problems you typically solve.
3. **Social Media Interactions**: Including content from LinkedIn posts, blog articles, and other professional interactions allows Memo-Mind to further enrich its understanding of your domain knowledge and areas of expertise.

Currently, the prototype is focused on processing Obsidian notes. Future iterations aim to include other data sources, enabling a more comprehensive digital twin experience.

## Features

- **Context-Aware Conversations**: Memo-Mind understands your previous interactions and the relationships between your notes, providing more accurate and relevant responses during a conversation.
- **Personalized Content Creation**: Whether you need content ideas, summaries, or even drafts for blog posts, Memo-Mind generates suggestions and outputs that match your writing style and subject matter expertise.
- **Smart Revision Assistance**: Helps you revisit old notes or study materials, summarizing key points, creating flashcards, and providing quizzes to reinforce learning.
- **Interview Preparation and Coding Help**: Offers interview-related questions and answers based on your knowledge, as well as tips on coding and system design, utilizing your past experiences and coding style.
- **Extensible Knowledge Base**: Easily expand Memo-Mind to incorporate new data sources, such as GitHub repositories or social media content, for a richer digital twin experience.

## Technical Overview

Memo-Mind is built using the RAG (Retrieval-Augmented Generation) framework, which combines vector-based search and generative AI for answering queries:
1. **Vector Store**: Uses Qdrant as the vector database to store embeddings of your content, enabling efficient vector search and context-aware retrieval.
2. **Generative AI**: LLMs are used for generating responses based on the retrieved information.
3. **LangChain for Pipeline Management**: LangChain manages the data flow, from retrieving relevant information from the vector store to generating final responses.

### Current Prototype

- **Data Source**: Currently integrates with Obsidian notes in markdown format. Since markdown is one of the formats LLMs are trained on they can respond and understand markdown very well. 
- **Knowledge Assistant Features**: Acts as a content idea generator, summarizer, and personal tutor for various tasks like revision, blog writing, and interview preparation.

### Output

The chatbot provides responses in natural language, mimicking your writing style and tone. It can generate content summaries, answer questions, provide explanations, and offer suggestions based on your notes and interactions.

Below I've chosen the `Blogs or Article Writing` prompt to generate a response:


## Getting Started

1. **Prerequisites**: Make sure you have Qdrant and Obsidian installed locally. Optionally, set up integrations for GitHub and other data sources for future expansion.
2. **Configuration**: Configure your local environment to point Memo-Mind to the directory where your Obsidian notes are stored.
3. **Running Memo-Mind**: Use the Streamlit app to interact with the chatbot. Choose from the custom prompts to get personalized responses based on your notes.


## Future Plans

- **Social Media and Code Integrations**: Expand support for LinkedIn, Medium, and GitHub data to make the digital twin even more comprehensive.
- **Advanced Fine-Tuning**: Fine-tune the generative models to better reflect your specific tone, domain expertise, and writing style.
- **Knowledge Expansion**: Incorporate external resources (e.g., research papers, online articles) to further enhance the chatbot's understanding and provide deeper insights.
