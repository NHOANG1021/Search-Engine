from bs4 import BeautifulSoup
import json
import re
from nltk.tokenize import word_tokenize

def extract_contents(file_path: str):
    """
    Given a json file path, returns the url and html content
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    return content

def extract_text(html_content):
    """
    Extracts all text from the given HTML content.
    """
    # add weights for BOLD, TITLES, HEADERS
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def tokenize_text(text):
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()
    return word_tokenize(clean_text)

