import requests
from bs4 import BeautifulSoup
from google import genai


def fetch_webpage_text(url):
    """
    Function to fetch and extract text from a webpage
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Error: Unable to fetch the webpage. Status Code: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")

    extracted_text = "\n".join([p.get_text() for p in soup.find_all(["p", "h1", "h2", "h3"])])

    return extracted_text[:5000]

def gemini(key, url) -> str:
    client = genai.Client(api_key=key)
    query = f'Provide a brief summary of the contents within this url after you read through it {url} make sure the name is correct and tell me his education'
    response = client.models.generate_content(model="gemini-2.0-flash", contents=f'{query}')

    return response.candidates[0].content.parts[0].text

def summarize_webpage(api_key, url):
    page_text = fetch_webpage_text(url)
    
    if "Error" in page_text:
        return page_text

    summary = gemini(api_key, page_text)
    return summary