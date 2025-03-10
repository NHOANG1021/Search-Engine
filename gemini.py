import requests
from bs4 import BeautifulSoup
from google import genai


def gemini(key: str, page_content: str) -> str:
    """
    Uses Gemini API to summarize the webpage content.
    """
    client = genai.Client(api_key=key)
    query = (f"Summarize this text in a three sentences, if the page is lacking)"
            f"in information or you do not see any text after the ampersand respond with 'This page is lacking enough information for a summary' & {page_content}")
    
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=query)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def summarize_webpage(api_key: str, resp: str) -> str:
    """
    Fetches webpage content and returns an AI-generated summary.
    """
    soup = BeautifulSoup(resp, "html.parser")
    extracted_text = "\n".join([p.get_text() for p in soup.find_all(["p", "h1", "h2", "h3"])])
    page_content = extracted_text[:5000]
    if "Error" in page_content:
        return page_content
    return gemini(api_key, page_content)


