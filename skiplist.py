import json
import heapq
from itertools import islice
from pathlib import Path

def generate_skipdict(posting_file: str, output_file: str) -> None:
    starting_characters = {}
    line_count = 0
    with open(posting_file, "r", encoding="utf-8") as f:

        for line in f:
            temp = json.loads(line)
            token = list(temp.keys())
            if token[0][0] not in starting_characters:
                starting_characters[token[0][0]] = line_count
            line_count += 1

    keys = list(starting_characters)
    length = len(keys) - 1
    for index, key in enumerate(starting_characters):
        if index < length:
            starting_characters[key] = (starting_characters[key], starting_characters[keys[index + 1]] + 1)
        else:
            starting_characters[key] = (starting_characters[key], line_count + 1)

    with open(output_file, "w", encoding = "utf-8") as out:
        json.dump(starting_characters, out, indent=4)

def load_index_line(line_num: int, posting_file: iter) -> tuple | None:
    line = next(islice(posting_file, line_num, None), None)
    if line is None:
        return None
    temp_dict = json.loads(line)
    token = list(temp_dict.keys())[0]
    return token, temp_dict[token]

def load_skip_dict(file_name: str) -> dict:
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_jsonl_section(file_path, start, end):
    """
    Reads a specific section of a JSONL file using itertools.islice.
    
    :param file_path: Path to the JSONL file.
    :param start: The starting line index (0-based).
    :param end: The ending line index (exclusive).
    :return: A list of dictionaries within the specified range.
    """
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in islice(file, start, end):  # Read only the required section
            data.append(json.loads(line))  
    return data

class Searcher:

    def __init__(self, index_file: str):
        if not Path("resources").exists():
            Path("resources").mkdir(parents=True, exist_ok=True)
        if not Path("resources/skip_dict.json").exists():
            generate_skipdict(index_file,"resources/skip_dict.json")
        self_loaded_section = []
        self.skip_dict = load_skip_dict("resources/skip_dict.json")

    def get_postings(tokens: set):
        curr_section = None
        for token in tokens:
            first_letter = token[0]
            if curr_section is None or first_letter != curr_section:
                curr_section = first_letter



    # Priority queue

    def priority_queue(postings: dict):
        min_heap = []

        for term, posting_list in postings.items():
            heapq.heappush(min_heap, (len(posting_list), term, posting_list))

        # Print the min-heap in order of posting list length
        while min_heap:
            length, term, posting_list = heapq.heappop(min_heap)
            print(f"Term: {term}, Posting List Length: {length}, Posting List: {posting_list}") 