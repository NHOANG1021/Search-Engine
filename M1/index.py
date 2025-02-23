#Postings look like (DocID: int, Frequency)

import json
from pathlib import Path
from collections import defaultdict
from csv import writer

def update_id_map(doc_id: int, url: str, csv_file: str) -> None:
    """
    Opens up a csv file to use as a map for doc ids and urls
    """
    with open(csv_file, 'a', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerow([doc_id, url])

def update_partial_index(partial: defaultdict, token_frequency: dict, doc_id: int):
    """
    Updates the partial dict by adding the postings for each token
    """
    for freq_pair in token_frequency:
        partial[freq_pair[0]].append(doc_id, freq_pair[1])

def dump_partial_index(json_file: str, partial_index: dict):
    """
    Dumps the partial index into a file on the disk
    """
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(partial_index, file, indent=4)

class Indexer:
    def __init__(self):
         directory = Path("/partial_indexes")
         directory.mkdir(parents=True, exist_ok=True)
         curr_doc_id = 0
         pages_read = 0
         index_files = []
         partial_index = defaultdict(list)

    def run(self, files: iter):
        pass