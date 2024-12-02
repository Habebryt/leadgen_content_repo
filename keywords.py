import requests
from bs4 import BeautifulSoup
import time

def listen_for_keywords(urls, keywords, delay=60):
    """
    Monitors the provided URLs for the specified keywords and prints any matches.
    
    Parameters:
    urls (list): A list of URLs to monitor
    keywords (list): A list of keywords to search for
    delay (int): The number of seconds to wait between checks (default is 60 seconds)
    """
    while True:
        for url in urls:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                text = soup.get_text().lower()
                
                for keyword in keywords:
                    if keyword.lower() in text:
                        print(f"Found '{keyword}' on {url}")
            except:
                print(f"Error accessing {url}")
        
        print("Waiting for next check...")
        time.sleep(delay)

# Example usage
urls = ["https://www.linkedin.com", "https://www.twitter.com"]
keywords = ["python", "web scraping", "automation"]
listen_for_keywords(urls, keywords)