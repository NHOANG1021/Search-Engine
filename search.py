import json
import mmap
from pathlib import Path
from bisect import bisect_left
import time

def build_offset_index(jsonl_file: str, index_file: str, step: int = 1000) -> None:
    """
    Creates an byte offset index for every 'step' lines in the JSONL file.
    """
    offsets = {}
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        # Get starting position
        position = f.tell()
        i = 0
        while True:
            line = f.readline()
            # End of file exit
            if not line:
                break
            # Every few steps load the position into the dict
            if i % step == 0:  
                entry = json.loads(line)
                key = entry['key']
                offsets[key] = position
            # Update position for next iteration
            position = f.tell()  
            # Update line counting
            i += 1  

    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(offsets, f)

def build_csv_offset_index(csv_file: str, index_file: str, step: int = 1000):
    """
    Creates an index mapping docIDs (line numbers) to byte offsets in the CSV file.
    """
    offsets = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        # Get starting position
        position = f.tell()
        i = 0
        while True:
            line = f.readline()
            # End of file exit
            if not line:
                break
            # Every few steps load the position into the dict
            if i % step == 0:  
                id_pair = line.split(',')
                offsets[int(id_pair[0])] = position
            # Update position for next iteration
            position = f.tell()  
            # Update line counting
            i += 1  

    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(offsets, f)

class Searcher:
    """
    Class created to handle the searching for given queries
    """
    def __init__(self, index_file: str, id_map: str):
        if not Path("resources").exists():
            Path("resources").mkdir(parents=True, exist_ok=True)
        if not Path("resources\\index_offsets.json").exists():
            build_offset_index(index_file, "resources\\index_offsets.json")
        if not Path("resources\\docid_offsets.json").exists():
            build_csv_offset_index(id_map, "resources\\docid_offsets.json")
        with open("resources\\index_offsets.json", 'r', encoding='utf-8') as f:
            self.offsets = json.load(f)
        with open("resources\\docid_offsets.json", 'r', encoding='utf-8') as f:
            self.docid_offsets =  json.load(f)
        self.offset_keys = list(self.offsets)
        self.docid_keys = [int(i) for i in list(self.docid_offsets)]
        self.index_file = index_file
        self.loaded_section = []
        self.current_char = None
        self.data_file = None
        self.id_map = id_map

    def __enter__(self):
        self.data_file = open(self.index_file, "r")
        self.id_map = open(self.id_map, "r")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.data_file:
            self.data_file.close()
        if self.id_map:
            self.id_map.close()

    def batch_find_postings(self, tokens: set) -> dict:
        """
        Find postings for a batch of tokens efficiently using a memory map
        """
        results = {}
        # Creates a memory mapped file that behaves like a byte array and is faster to read from
        with mmap.mmap(self.data_file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            for token in tokens:
                # Binary search to get the closest indexed key
                idx = bisect_left(self.offset_keys, token)
                
                # Get the starting index to search from
                start_idx = max(0, idx - 1) 
                start_key = self.offset_keys[start_idx]
                # Do a seek to get to where we want to start reading
                mm.seek(self.offsets[start_key])
                # Scan nearby lines
                for _ in range(10000): 
                    # Read and decode the line
                    line = mm.readline().decode('utf-8')
                    # Check if we have hit the end of the file
                    if not line:
                        break
                    # Load the json line and preform checks on the key
                    entry = json.loads(line)
                    key = entry['key']
                    # Early exit if we passed the token
                    if key > token:
                        break
                    # If we found the token add it to our results dict
                    if key == token:
                        results[token] = entry['posting']
                        break
                else:
                    # Token not found
                    results[token] = None 
        return results

    def conjunctive_search_set(self, tokens: set) -> dict:
        """
        Performs conjunctive query processing using set intersection.
        Returns a dictionary where keys are document IDs and values are lists of (token, frequency) pairs.
        """
        postings = self.batch_find_postings(tokens)

        # If any token has no postings return empty dict
        try:
            if any(postings[token] is None for token in tokens):
                return {}
        except KeyError:
            print ("Cannot find results")
            return {}

        # Convert postings to dicts for each token
        posting_dicts = {token: {doc_id: freq for doc_id, freq in postings[token]} for token in tokens}

        # Find common doc_ids in all posting lists using set intersection
        common_docs = set.intersection(*[set(posting_dicts[token].keys()) for token in tokens])

        # Build result dictionary with token, frequency pairs for each doc_id
        result_docs = {doc_id: [(token, posting_dicts[token][doc_id]) for token in tokens] for doc_id in common_docs}

        return result_docs
    
    def get_url_from_csv(self, docid: int) -> str:
        # Creates a memory mapped file that behaves like a byte array and is faster to read from
        with mmap.mmap(self.id_map.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            # Binary search to get the closest indexed key
            idx = bisect_left(self.docid_keys, docid)
            docid = str(docid)
            # Get the starting index to search from
            start_idx = max(0, idx - 1) 
            start_key = self.docid_keys[start_idx]
            # Do a seek to get to where we want to start reading
            mm.seek(self.docid_offsets[str(start_key)])
            # Scan through lines
            while True:
                # Read and decode the line
                line = mm.readline().decode('utf-8')
                # Check if we have hit the end of the file
                if not line:
                    break
                # Load the csv line and preform checks on the key
                entry = line.split(',')
                # If we found the token add it to our results dict
                if entry[0] == docid:
                    return entry[1]
            return None