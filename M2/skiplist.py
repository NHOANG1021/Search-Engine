import json
from itertools import islice

def generate_skipdict(posting_file: str, output_file: str) -> None:
    starting_characters = {}
    with open(posting_file, "r", encoding="utf-8") as f:
        line_count = 0
        for line in f:
            temp = json.loads(line)
            token = list(temp.keys())
            if token[0][0] not in starting_characters:
                starting_characters[token[0][0]] = line_count
            line_count += 1
        print(line_count)
    with open(output_file, "w", encoding = "utf-8") as out:
        json.dump(starting_characters, out, indent=4)

def load_index_line(line_num: int, posting_file: iter) -> tuple | None:
    line = next(islice(posting_file, line_num, None), None)
    if line is None:
        return None
    temp_dict = json.loads(line)
    token = list(temp_dict.keys())[0]
    return token, temp_dict[token]