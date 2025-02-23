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
    

def compute_word_frequncies(tokens: list) -> list:
    """
    Takes a list of tokens and returns a list of tuples
    with each tuple containing (word, frequency)
    """
    token_dict = {}
    for token in tokens:
        if token not in token_dict.keys():
            token_dict[token] = 1
        else:
            token_dict[token] += 1
            
    sorted_frequencies = sorted(token_dict.items(), key=lambda x: (x[0], -x[1]))
    return sorted_frequencies

def parse(file: str):
    """
    Calls all the necessary functions to parse
    """
    content = tokenizer.extract_contents(file)
    extracted_html_content = tokenizer.extract_text(content['content'])
    extracted_important_words = tokenizer.extract_special_text(content['content'])
    tokens = tokenizer.tokenize_text(extracted_html_content)
    important_tokens = tokenizer.tokenize_text(extracted_important_words)  # Use later
    stem_tokens =  tokenizer.porter_stem(tokens)
    frequencies = compute_word_frequncies(stem_tokens)

    return frequencies
