import os
import re
import json
from datetime import datetime
import tqdm

class NoteProcessor:
    def __init__(self, notes_dir):
        self.notes_dir = notes_dir
        self.notes_data = []
    
    
    def extract_notes(self):
        """
        Extract markdown files from the notes directory
        """
        # Get the list of all markdown files
        markdown_files = [filename for filename in os.listdir(self.notes_dir) if filename.endswith('.md')]
    
        # Use tqdm to create a progress bar while processing
        for filename in tqdm.tqdm(markdown_files):
            self.process_note_file(os.path.join(self.notes_dir, filename), filename.split('.')[0])
    
    
    def process_note_file(self, file_path, title):
        """
        Process a single markdown file ansd extract relevant information
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            metadata, body, references = self.split_note_content(content)
            note = self.parse_note_metadata(title, metadata, body, references)
            self.notes_data.append(note)
    
    
    def split_note_content(self, content):
        """
        Split the markdown content into metadata, body and references
        """
        if '---' in content:
            parts = content.split('---')
            metadata = parts[1].strip() if len(parts) > 1 else ''
            body = parts[2: -1]
            references = parts[-1].strip() if len(parts) > 1 else ''
            return metadata, body, references
        return '', content, ''
    
    
    def parse_note_metadata(self, title, metadata, body, references):
        """
        Parse the metadata of a note along with the body and references
        """
        note = {}
        note['title'] = title
        note['related_notes'] = self.extract_wikilinks(' '.join(body))
        note['related_notes'] += self.extract_wikilinks(references)
        note['content'] = self.extract_content(' '.join(body))
        note['references'] = self.extract_references(references)
        return note
    
    
    def extract_content(self, body):
        """
        Extract the content of the note
        """
        return body.strip()
    
    
    def extract_wikilinks(self, content):
        """
        Extract wikilinks from the note content
        """
        matches = re.findall(r'\[\[(.*?)\]\]', content)
        return [match for match in set(matches)]
    
    
    def extract_references(self, references):
        """
        Extract references to links from the note content
        """
        matches = re.findall(r'\[(.*?)\]\((.*?)\)', references)
        return [{'title': title, 'link': link} for title, link in matches]

    
    def save_to_json(self, output_file):
        """
        Save the notes data to a JSON file
        """
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(self.notes_data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    notes_dir = "/Users/admin/Library/CloudStorage/GoogleDrive-vsrikar44@gmail.com/My Drive/Second Brain/05-Zettelkasten"
    output_file = "/Users/admin/Documents/Github Repos/memo-mind/processed_notes.json"
    processor = NoteProcessor(notes_dir)
    processor.extract_notes()
    processor.save_to_json(output_file)