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
    Extracts only the words from title, headers, and bold tags from the given HTML content.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    title_text = soup.title.get_text(strip=True) if soup.title else ''
    header_text = ' '.join([element.get_text(strip=True) for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
    bold_text = ' '.join([element.get_text(strip=True) for element in soup.find_all(['b', 'strong'])])
    special_text = title_text + header_text + bold_text

    return special_text

def tokenize_text(text: str) -> list[str]:
    """
    Given a string, returns a list of only alphanumeric tokens
    """
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()
    return word_tokenize(clean_text)

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
