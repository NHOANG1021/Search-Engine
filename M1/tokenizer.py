from bs4 import BeautifulSoup
import json
import re
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import PorterStemmer 

def extract_contents(file_path: str) -> dict:
    """
    Given a json file path, simply loads and returns the content of the json
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    return content

def extract_text(html_content: str) -> str:
    """
    Extracts all text from the given HTML content.
    """
    # add weights for BOLD, TITLES, HEADERS
    soup = BeautifulSoup(html_content, 'lxml')
    return soup.get_text(separator=' ', strip=True)

# Not used yet
def extract_special_text(html_content):
    """
    Extracts text from title, headers, and bold tags using a streaming approach via descendants.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    title_text = soup.title.get_text(strip=True) if soup.title else ''
    header_text = []
    bold_text = []

    # Process the document as it is parsed, avoiding full searches
    for tag in soup.body.descendants:
        if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            header_text.append(tag.get_text(strip=True))
        elif tag.name in ['b', 'strong']:
            bold_text.append(tag.get_text(strip=True))

    header_text = ' '.join(header_text)
    bold_text = ' '.join(bold_text)
    special_text = f"{header_text} {bold_text}".strip()

    return title_text, special_text


def add_title_weight(frequencies, title_frequencies):
    """
    Calls the add_weight() helper function to increase the weight
    of title words by a factor of 3
    """
    return add_weight(frequencies, title_frequencies, 3)


def add_other_weight(frequencies, important_frequencies):
    """
    Calls the add_weight() helper function to increase the weight
    of header and bold words by a factor of 2
    """
    return add_weight(frequencies, important_frequencies, 2)


def add_weight(frequencies, weighted_frequencies, weight):
    """
    Given total frequencies, weighted frequencies, and a corresponding weight,
    returns and updated dictionary of frequencies with weights applied.
    """
    frequencies =  dict(frequencies)
    weighted_dict = dict(weighted_frequencies)

    for word in frequencies.keys():
        if word in weighted_dict:
            frequencies[word] *= weight
    
    return frequencies


def tokenGenerator(text: str):
    """
    Yields tokens that match regex pattern
    """
    token_maker = RegexpTokenizer(r'[a-zA-Z0-9]+')
    for token in token_maker.tokenize(text.lower()):
        yield token

def porter_stem(tokens: list[str]) -> list[str]:
    """
    Given a list of tokens performs porter stemming on each token
    """
    stemmer =  PorterStemmer()
    stemmed_words = [stemmer.stem(token) for token in tokens]
    return stemmed_words
