import json
import nltk
from heapq import merge
from tokenizer import extract_contents
from parse import parse
from pathlib import Path
from collections import defaultdict
from csv import writer

class Indexer:
    """
    Indexer is a class utilized to create partial indexes
    """
    def __init__(self):
        nltk.download('punkt')
        self.directory = Path("partial_indexes")
        self.directory.mkdir(parents=True, exist_ok=True)
        self.curr_doc_id = 1
        self.index_files = []
        self.partial_index = defaultdict(list)

    def update_partial_index(self, token_frequency: dict) -> None:
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

    def dump_partial_index(self, storage_file: str) -> None:
        """
        Dumps the partial index into a file on the disk with a more compact format
        Each line is a key-value pair in JSON format
        """
        with open(storage_file, "w", encoding="utf-8") as file:
            for key in sorted(self.partial_index.keys()):
                file.write(json.dumps({key: self.partial_index[key]}) + "\n")

    def make_partial_index(self) -> None:
        """
        Creates a txt file to store the partial index on disk and then resets the partial index, function generates
        and appends filenames to an array for later use
        """
        file_path = f"{self.directory}//{len(self.index_files)}.txt"
        self.dump_partial_index(file_path)
        self.partial_index = defaultdict(list)
        self.index_files.append(file_path)

    def file_line_generator(self, file_name):
        """
        Creates a generator that yields every line from the file as a dictionary
        """
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                if line:
                    yield json.loads(line)

    def load_partial_indexes(self) -> list:
        """
        Returns a list of iterators created from the partial index files
        """
        iterators = []
        for file_name in self.index_files:
            try:
                # Make generator and append it to list
                contents = self.file_line_generator(file_name)
                iterators.append(contents)
            except Exception as e:
                print(f"Error loading {file_name}: {e}")
        return iterators

    def merge_indexes(self, iterators):
        """
        Uses heapq merge to merge all the sorted iterators by their key value into one singular iterator by utilizing a minheap.
        This will run in O(N log K) time as where N is the total number of elements and K is the number of iterators. 
        The log comes from the fact that heap operations need to be used on the iterators.
        """
        return merge(*iterators, key=lambda x: list(x.keys())[0])

    def process_merged_index(self, merged_index, output_file):
        """
        Processes the merged index by combining postings for the same token and writes the final index into a file in JSON Lines format
        """
        current_token = None
        current_postings = []

        with open(output_file, "w", encoding="utf-8") as output:
            for entry in merged_index:
                # Extract token and postings
                token, postings = list(entry.items())[0]  
                if token != current_token:
                    # Check if there is a previous token
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
        # Loads partial indexes into a list of iterators
        iterators = self.load_partial_indexes()
        # Merges iterators into a single sorted iterator
        merged_index = self.merge_indexes(iterators)
        # Processes and creates the final merged index onto disk
        self.process_merged_index(merged_index, output_file)


    def run(self, files: iter):
        """
        Using an iterator of files, goes through each file within a directory and creates an inverted index into a jsonl file
        """
        # Go through every file in the iterable
        for file in files:
            # Every 500 files generate a new partial index file
            if (self.curr_doc_id % 250 == 0):
                self.make_partial_index()
            
            # Extract contents from a file and then parse it and update the partial index in memory
            contents = extract_contents(file)
            tokens = parse(contents["content"])
            self.update_partial_index(tokens)
            # Updates the id mpa and and increments the doc id
            self.update_id_map(contents["url"], "doc_id_map.csv")
            self.curr_doc_id += 1
        
        # Makes the last partial index
        if self.partial_index:
            self.make_partial_index()
        # Merges all partial indexes
        self.merge_partial_index("final.jsonl")