import os
import tokenizer


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
        if token not in token_dict.keys():
            token_dict[token] = 1
        else:
            token_dict[token] += 1
            
    sorted_frequencies = sorted(token_dict.items(), key=lambda x: (x[0], -x[1]))
    return sorted_frequencies


def parse(file: str):
    """
    Calls all the necessary functions to parse on all tokens,
    title tokens, and other important tokens (header and bolded).
    """
    content = tokenizer.extract_contents(file)
    extracted_html_content = tokenizer.extract_text(content['content'])
    title_text, important_text = tokenizer.extract_special_text(content['content'])

    tokens = tokenizer.tokenize_text(extracted_html_content)
    title_text = tokenizer.tokenize_text(title_text)
    important_tokens = tokenizer.tokenize_text(important_text)

    stem_tokens =  tokenizer.porter_stem(tokens)
    title_stem_tokens = tokenizer.porter_stem(title_text)
    important_stem_tokens = tokenizer.porter_stem(important_tokens)

    frequencies = compute_word_frequncies(stem_tokens)
    title_frequencies = compute_word_frequncies(title_stem_tokens)
    important_frequencies = compute_word_frequncies(important_stem_tokens)

    weighted_frequencies1 = tokenizer.add_title_weight(frequencies, title_frequencies)
    weighted_frequencies2 = tokenizer.add_other_weight(weighted_frequencies1, important_frequencies)


    return weighted_frequencies2
