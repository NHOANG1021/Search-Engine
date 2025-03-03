import os
import tokenizer
from sortedcontainers import SortedSet


def traverse_directory(root: str) -> iter:
    """
    Given a file path, recursively traverses a directory and returns a list of all .json files.
    """
    for root, dirs, files in os.walk(root):
        for file in files:
            yield os.path.join(root, file)

def compute_word_frequncies(tokens: list) -> list:
    """
    Takes a list of tokens and returns a list of tuples
    with each tuple containing (word, frequency)
    """
    token_dict = {}
    for token in tokens:
        if token not in token_dict:
            token_dict[token] = 1
        else:
            token_dict[token] += 1
            
    return token_dict

def parse(content: str):
    """
    Calls all the necessary functions to parse on all tokens,
    title tokens, and other important tokens (header and bolded).
    """
    extracted_html_content = tokenizer.extract_text(content)
    title_text, important_text = tokenizer.extract_special_text(content)
    tokens = tokenizer.tokenGenerator(extracted_html_content)

    tokens = tokenizer.tokenGenerator(extracted_html_content)
    title_text = tokenizer.tokenGenerator(title_text)
    important_tokens = tokenizer.tokenGenerator(important_text)

    stem_tokens =  tokenizer.porter_stem(tokens)
    title_stem_tokens = tokenizer.porter_stem(title_text)
    important_stem_tokens = tokenizer.porter_stem(important_tokens)

    frequencies = compute_word_frequncies(stem_tokens)
    title_frequencies = compute_word_frequncies(title_stem_tokens)
    important_frequencies = compute_word_frequncies(important_stem_tokens)

    weighted_frequencies1 = tokenizer.add_title_weight(frequencies, title_frequencies)
    weighted_frequencies2 = tokenizer.add_other_weight(weighted_frequencies1, important_frequencies)


    return weighted_frequencies2

def process_query(query: str) -> dict:
    """
    Returns a dictionary of stemmed words from a user's query
    """
    tokens = tokenizer.tokenGenerator(query)
    stemmed_tokens = tokenizer.porter_stem(tokens)
    return SortedSet(stemmed_tokens)
