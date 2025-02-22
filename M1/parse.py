from bs4 import BeautifulSoup
import os
import json
#12:33

def traverse_directory(root: str) -> list[str]:
    """
    Given a file path, recursively traverses a directory and returns a list of all .json files.
    """
    total_files = []
    for root, dirs, files in os.walk(root):
        for file in files:
            total_files.append(os.path.join(root, file))
        for dir in dirs:
            os.path.join(root, dir)
    
    return total_files

def parse_all(total_files: list[str]):
    data = {}
    doc_id = 0
    for file in total_files:
        url, html_content = extract_contents(file)
        extracted_html_content = extract_text(html_content)
        data[doc_id] = url, extracted_html_content
        doc_id += 1
        print(doc_id)
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def extract_contents(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    return content['url'] , content['content']

def extract_text(html_content):
    """
    Extracts all text from the given HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)
