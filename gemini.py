import requests
from bs4 import BeautifulSoup
from google import genai


def fetch_webpage_text(url: str) -> str:
    """
    Function to fetch and extract text from a webpage given a URL.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    # Handle redirects or client side errors
    if response.status_code != 200:
        return f"Error: Unable to fetch the webpage. Status Code: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    extracted_text = "\n".join([p.get_text() for p in soup.find_all(["p", "h1", "h2", "h3"])])
    
    # Make sure to adhere to Gemini's 5000 word limit
    return extracted_text[:5000]

def gemini(key: str, page_content: str) -> str:
    """
    Given an api key and page content, utilizes Gemini API
    to generate and return a summary of the page content
    """
    client = genai.Client(api_key=key)
    query = f'Provide a brief summary of this text {page_content}'
    response = client.models.generate_content(model="gemini-2.0-flash", contents=f'{query}')

    return response.candidates[0].content.parts[0].text

def summarize_webpage(api_key: str, url: str) -> str:
    """
    Functiion that, when given an api key and url, returns an AI generated summary of the web page.
    """
    page_content = fetch_webpage_text(url)
    if "Error" in page_content:
        return page_content

    summary = gemini(api_key, page_content)
    return summary