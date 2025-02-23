import os
import tokenizer

def traverse_directory(root: str) -> iter:
    """
    Given a file path, recursively traverses a directory and returns a list of all .json files.
    """
    for root, dirs, files in os.walk(root):
        for file in files:
            yield os.path.join(root, file)
        for dir in dirs:
            os.path.join(root, dir)

def compute_word_frequencies(tokens: list) -> list:
    token_dict = {}
    for token in tokens:
        if token not in token_dict.keys():
            token_dict[token] = 1
        else:
            token_dict[token] += 1
            
    return token_dict

def parse(content: str):
    extracted_html_content = tokenizer.extract_text(content)
    tokens = tokenizer.tokenize_text(extracted_html_content)
    frequencies = compute_word_frequencies(tokens)
    
    return frequencies
