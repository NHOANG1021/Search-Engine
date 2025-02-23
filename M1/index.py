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
                self.partial_index[token].append([self.curr_doc_id, freq])  # Use a tuple instead of a set

    def update_id_map(self, url: str, csv_file: str) -> None:
        """
        Opens up a csv file to use as a map for doc ids and urls
        """
        with open(csv_file, 'a+', newline='') as f:
            csv_writer = writer(f)
            csv_writer.writerow([self.curr_doc_id, url.strip('"')])

    def dump_partial_index(self, json_file: str):
        """
        Dumps the partial index into a file on the disk with a more compact format.
        """
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(self.partial_index, file, separators=(",", ": "))

    def make_partial_index(self):
        file_path = f"{self.directory}//{len(self.index_files)}.json"
        self.dump_partial_index(file_path)
        self.partial_index = defaultdict(list)
        self.index_files.append(file_path)

    def load_partial_indexes(self):
        iterators = []
        opened_files = []
        for file_name in self.index_files:
            try:
                file = open(file_name, "r")
                opened_files.append(file)
                data = json.load(file)
                iterators.append(data.items())
            except Exception as e:
                print(f"Error loading {file_name}: {e}")
        return iterators, opened_files

    def merge_indexes(self, iterators):
        return merge(*iterators)

    def process_merged_index(self, merged_index):
        final_index = {}
        current_term = None
        current_postings = []

        for term, postings in merged_index:
            if term != current_term:
                if current_term is not None:
                    # Deduplicate and sort the postings list
                    final_index[current_term] = current_postings
                current_term = term
                current_postings = postings
            else:
                current_postings.extend(postings)

        # Add the last term
        if current_term is not None:
            final_index[current_term] = current_postings
        
        return final_index

    def merge_partial_index(self, output_file):
        iterators, opened_files = self.load_partial_indexes()
        merged_index = self.merge_indexes(iterators)
        final_index = self.process_merged_index(merged_index)

        try:
            with open(output_file, "w", encoding="utf-8") as output:
                json.dump(final_index, output, separators=(",", ": "))
        finally:
            for file in opened_files:
                file.close()

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

        self.merge_partial_index("final.json")