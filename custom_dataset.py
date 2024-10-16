import google.generativeai as genai #type: ignore
import csv
import json
import re
import tqdm
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

PROMPT_TEMPLATE = """
Your task is to create a question and answer pair based on the content provided. 
You are an expert in explaining concepts and generating content for educational purposes.
The answer must be more detailed and explanatory including examples or illustrations.
I want the answer to be structured and not just one-liners or sentences, you can include summary or key points in the answer.
Include questions that test the understanding of the concepts and provide detailed answers to help the learner grasp the topic effectively.
Generate only one question and answer pair.
Content:
{content}   

Question: ...
Answer: ...
...
"""


def parse_output_single_qa(response_text):
    """
    Parses the response text to extract a single question and answer pair.
    """
    # Split based on "Question" and "Answer" keywords
    question_marker = "Question:"
    answer_marker = "Answer:"
    
    # Find the indices of the markers in the text
    question_index = response_text.find(question_marker)
    answer_index = response_text.find(answer_marker)
    
    # If both markers are found, extract the text between them
    if question_index != -1 and answer_index != -1:
        question = response_text[question_index + len(question_marker):answer_index].strip()
        answer = response_text[answer_index + len(answer_marker):].strip()
        return {"question": question, "answer": answer}
    
    # If the markers aren't found or if the output doesn't match the expected format
    return None

def generate_qa_pairs(docs):
    qa_pairs = []
    for doc in tqdm.tqdm(docs):
        # Format the prompt with the current content
        prompt = PROMPT_TEMPLATE.format(content=doc['content'])

        # Generate the response using the Gemini model
        response = genai.GenerativeModel("gemini-1.5-flash-8b").generate_content(
            prompt
        )
        try: 
            # Parse the response to extract the Q&A pairs
            qa_pair = parse_output_single_qa(response.text)
        except Exception as e:
            print(f"Error processing document: {doc['title']}")
            print(f"Error: {e}")
            qa_pair = None
        # If a valid Q&A pair is found, add it to the list
        if qa_pair:
            qa_pairs.append(qa_pair)
    return qa_pairs

def save_qa_pairs_to_csv(qa_pairs, output_file="qa_pairs.csv"):
    # Save the generated Q&A pairs to a CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["question", "answer"])
        writer.writeheader()
        writer.writerows(qa_pairs)

def main():
    # Load your parsed chunks from a JSON file or directly as a list
    with open("processed_notes.json", "r") as file:
        docs = json.load(file)

    # Generate Q&A pairs using the Gemini model
    qa_pairs = generate_qa_pairs(docs)

    # Save the generated Q&A pairs to a CSV file for fine-tuning
    save_qa_pairs_to_csv(qa_pairs, "qa_pairs_for_finetuning.csv")
    print("Q&A pairs generated and saved successfully.")

if __name__ == "__main__":
    main()