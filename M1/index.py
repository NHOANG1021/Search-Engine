import json
import nltk
from heapq import merge
from tokenizer import extract_contents
from parse import parse
from pathlib import Path
from collections import defaultdict
from csv import writer

class Indexer:
    def __init__(self):
        nltk.download('punkt_tab')
        self.directory = Path("partial_indexes")
        self.directory.mkdir(parents=True, exist_ok=True)
        self.curr_doc_id = 1
        self.index_files = []
        self.partial_index = defaultdict(list)

    def update_partial_index(self, token_frequency: dict):
        """
        Updates the partial dict by adding the postings for each token
        """
        for token, freq in token_frequency.items():
                self.partial_index[token].append([self.curr_doc_id, freq])

    def update_id_map(self, url: str, csv_file: str) -> None:
        """
        Opens up a csv file to use as a map for doc ids and urls
        """
        with open(csv_file, 'a+', newline='') as f:
            csv_writer = writer(f)
            csv_writer.writerow([self.curr_doc_id, url])

    def dump_partial_index(self, storage_file: str):
        """
        Dumps the partial index into a file on the disk with a more compact format.
        Each line contains a key-value pair in JSON format.
        """
        with open(storage_file, "w", encoding="utf-8") as file:
            for key in sorted(self.partial_index.keys()):
                file.write(json.dumps({key: self.partial_index[key]}) + "\n")

    def make_partial_index(self):
        file_path = f"{self.directory}//{len(self.index_files)}.txt"
        self.dump_partial_index(file_path)
        self.partial_index = defaultdict(list)
        self.index_files.append(file_path)

    def file_line_generator(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                if line:
                    yield json.loads(line)

    def load_partial_indexes(self):
        iterators = []
        for file_name in self.index_files:
            try:
                contents = self.file_line_generator(file_name)
                iterators.append(contents)
            except Exception as e:
                print(f"Error loading {file_name}: {e}")
        return iterators

    def merge_indexes(self, iterators):
        return merge(*iterators, key=lambda x: list(x.keys())[0])

    def process_merged_index(self, merged_index, output_file):
        current_token = None
        current_postings = []

        with open(output_file, "w", encoding="utf-8") as output:
            for entry in merged_index:
                token, postings = list(entry.items())[0]  # Extract token and postings
                if token != current_token:
                    if current_token is not None:
                        # Write the postings for the previous token to the output file
                        output.write(json.dumps({current_token: current_postings}) + "\n")
                    # Start a new token
                    current_token = token
                    current_postings = postings
                else:
                    # Extend the postings for the current token
                    current_postings.extend(postings)

            # Write the last token's postings to the output file
            if current_token is not None:
                output.write(json.dumps({current_token: current_postings}) + "\n")

    def merge_partial_index(self, output_file):
        """
        Merges all partial indexes into a final index and writes it to the output file incrementally.
        """
        iterators = self.load_partial_indexes()
        merged_index = self.merge_indexes(iterators)
        self.process_merged_index(merged_index, output_file)


    def run(self, files: iter):
        for file in files:

            if (self.curr_doc_id % 500 == 0):
                self.make_partial_index()
            
            contents = extract_contents(file)
            tokens = parse(contents["content"])
            self.update_partial_index(tokens)
            self.update_id_map(contents["url"], "doc_id_map.csv")
            self.curr_doc_id += 1
        
        if self.partial_index:
            self.make_partial_index()

        self.merge_partial_index("final.jsonl")