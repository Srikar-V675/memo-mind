import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import google.generativeai as genai  # type: ignore
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# Configure API key for Google Gemini
load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

embedding_model_name = 'BAAI/bge-large-en'
embedding_model = HuggingFaceBgeEmbeddings(model_name=embedding_model_name)

# Initialize Qdrant vector store
qdrant_url = "http://localhost:6333"  # Replace with your Qdrant URL
collection_name = "vector_db"  # Replace with your Qdrant collection name
client = QdrantClient(url=qdrant_url)
db = Qdrant(
    client=client,
    embeddings=embedding_model,
    collection_name=collection_name
)

# Create a Google Generative AI model instance
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", api_key=API_KEY)

# Define prompts for different tasks (if needed)
PROMPTS = {
    "None": "",
    "Content Creation Ideas": 
        """
        You are a skilled content creator tasked with generating engaging content ideas on the given topic or user query. 
        Your goal is to provide a list of unique, interesting, and informative content ideas that can captivate the target audience. 
        For each idea, include the following:
        
        1. **Title or Topic**: A catchy or descriptive title for the content idea.
        2. **Description**: A brief explanation of the content, including its relevance and potential impact on the audience.
        3. **Outline or Key Points**: A list of main points or sections that should be covered.
        4. **Formats and Media Suggestions**: Indicate where to include visuals, diagrams, code snippets, or interactive elements.

        Make sure each idea is distinct, relevant to the topic, and encourages creativity.
        Format:
        - **Idea 1 Title**: ...
            - **Description**: ...
            - **Outline**: ...
            - **Suggested Media**: ...
        - **Idea 2 Title**: ...
        ...
        """,
    "Blogs or Article Writing": 
        """
        You are an expert technical writer assigned to craft a comprehensive and engaging blog post or article on the provided topic or user query.
        The content should be structured with clear sections or subtopics, each containing in-depth explanations, examples, and references. 
        Follow these guidelines:

        1. **Introduction**: Provide a brief introduction that hooks the reader and introduces the topic.
        2. **Section/Subtopic Structure**: Divide the content into logical sections with headings.
            - For each section:
                - **Heading**: Clearly defined heading for the section.
                - **Content**: Detailed explanations, real-world examples, or use cases.
                - **Visuals**: Indicate where to add images, diagrams, or code snippets.
        3. **Conclusion**: Summarize the key points and include a call to action or final thoughts.
        4. **References or Citations**: Include any sources or additional reading material.

        The tone should be casual and include storytelling elements to make the content engaging.
        Use Markdown formatting:
        - **Heading Format**: `#` for main titles, `##` for sections, etc.
        - **Lists and Bullet Points**: Use `-` or `*`.
        ...
        """,
    "Summary": 
        """
        You are a summarizer tasked with condensing the given content into a concise and comprehensive summary.
        Follow these steps to ensure the summary captures the main ideas, essential details, and key points:

        1. **Main Ideas**: Highlight the primary themes or arguments.
        2. **Supporting Details**: Include relevant facts, examples, or data.
        3. **Important Concepts**: Summarize any significant terms or concepts that need to be understood.

        The summary should be in bullet points or numbered list format, making it easy to read and absorb. 
        If applicable, include a brief concluding remark to wrap up the content.
        Format:
        - **Main Idea 1**: ...
            - **Key Point**: ...
        - **Main Idea 2**: ...
        ...
        """,
    "Question and Answer": 
        """
        You are a quiz creator tasked with developing a comprehensive set of questions and answers based on the given content.
        The questions should test various aspects, from basic understanding to deeper insights, and should challenge the reader's knowledge.

        For each question:
        1. **Question Type**: Indicate if it's multiple-choice, open-ended, scenario-based, etc.
        2. **Question Text**: Clearly stated question.
        3. **Answer Explanation**: Provide a detailed answer, including examples or additional insights.
        4. **Follow-up or Related Questions**: Suggest related questions to further test understanding.

        Use Markdown formatting:
        - **Question Format**: `### Q1: ...`
        - **Answer Format**: Use collapsible sections to hide/show answers.
        - **Toggle Buttons**: Implement toggles for each answer.

        Example Format:
        ### Q1: What is the primary benefit of using AI for content generation?
        - **Type**: Multiple Choice
        - **Answer**: <details><summary>Show Answer</summary>AI helps in automating content creation, reducing manual effort, and generating data-driven insights.</details>
        ...
        """,
    "Interview Prep": 
        """
        You are a job interview coach preparing a set of technical interview questions based on the content provided.
        The questions should evaluate a candidate's depth of knowledge and problem-solving skills, focusing on real-world applications.

        1. **Question Format**:
            - **Technical/Conceptual**: Explain concepts in detail.
            - **Scenario-Based**: Describe a problem that requires a solution.
            - **Coding Challenge**: Provide a coding problem with expected outputs.

        2. **Answers**:
            - **Detailed Explanation**: Explain using the STAR format (Situation, Task, Action, Result).
            - **Tips**: Provide additional advice or common mistakes to avoid.

        Markdown formatting for organization:
        - **Question Heading**: `### Q1: ...`
        - **Answer**: Use collapsible sections to show/hide detailed answers.
        Format:
        ### Q1: Describe the STAR format for answering interview questions.
        - **Answer**: <details><summary>Show Answer</summary>The STAR format stands for ...</details>
        ...
        """,
    "Revision": 
        """
        You are a student preparing for an exam and need to revise the following content. 
        Your task is to create concise and effective revision materials:

        1. **Summaries**: Provide a brief overview of each section.
        2. **Flashcards**: Formulate questions and answers for key terms or concepts.
        3. **Mind Maps or Concept Maps**: Describe visual tools that can help remember important information.
        4. **Self-Assessment Questions**: Include questions for the student to test their understanding.

        The revision content should be easy to understand and cover all crucial topics.
        Use Markdown for organization:
        - **Summary Format**: Bullet points or numbered lists.
        - **Flashcards**: Use toggles to hide/show the answers.
        Example:
        **Flashcard 1**: What is a vector database?
        - <details><summary>Show Answer</summary>A vector database stores ...</details>
        ...
        """
}


# Streamlit app layout
st.title("Memo-Mind")
st.sidebar.markdown("# Description")
st.sidebar.markdown("Welcome to Memo-Mind, a conversational RAG chatbot designed to assist with content creation, summarization, question generation, and more. The RAG component leverages my obsidian notes and the Google Generative AI model to provide context-aware responses with respect to custom prompts given below.")
st.sidebar.markdown("# Custom Prompts")

# User inputs
selected_task = st.sidebar.selectbox("Select a Prompt", list(PROMPTS.keys()))

# Initialize RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=model,
    retriever=db.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 10, 'lambda_mult': 0.25}    
    ),
    chain_type="stuff",  # or another suitable type based on your needs
    return_source_documents=True  # Optional: if you want to return source documents as well
)

# Function to construct prompt using the selected task, chat history, and user query
def build_prompt(user_query, chat_history, task_prompt):
    # Format chat history into a string
    history_str = "\n".join([f"User: {msg.content}" if isinstance(msg, HumanMessage) else f"AI: {msg.content}"
                             for msg in chat_history])

    # Construct the final prompt
    prompt = f"""
    Chat history:
    {history_str}

    {task_prompt}
    
    User question:
    {user_query}

    Refer to the chat history for context. Use task prompt to generate a response based on the user query and retrieved information.
    """
    # st.write(prompt)
    return prompt

# Function to get a response using the RAG approach
def get_response(user_query):
    # Build the custom prompt with chat history and selected task
    task_prompt = PROMPTS[selected_task]
    custom_prompt = build_prompt(user_query, st.session_state.chat_history, task_prompt)

    # Generate response using the RetrievalQA chain
    result = qa_chain({"query": custom_prompt})
    return result["result"], result.get("source_documents", [])


# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

# Display conversation history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# User input handling
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response, source_docs = get_response(user_query)
        st.markdown(response)

        # Optionally display source documents if needed
        if source_docs:
            related_notes = set()
            references = set()
            for doc in source_docs[:2]:
                for note in doc.metadata.get("related_notes", []):
                    if '.excalidraw' in note:
                        continue
                    related_notes.add(note)
                for ref in doc.metadata.get("references", []):
                    link = f"[{ref['title']}]({ref['link']})"
                    references.add(link)
            related_notes = [f'`{note}`' for note in related_notes]
            references = [f"{i+1}. {ref}" for i, ref in enumerate(references)]
            st.markdown("#### Related Notes: ")
            st.markdown(", ".join(related_notes))
            st.markdown("#### References: ")
            for ref in references:
                st.markdown(ref)

    st.session_state.chat_history.append(AIMessage(content=response))
