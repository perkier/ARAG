import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.fetch_html()
    
    def fetch_html(self):
        """Fetches the HTML content of the given URL."""
        headers = {'User-Agent': 'Mozilla/5.0'}  # Avoid getting blocked by some websites
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception(f"Failed to fetch page: {response.status_code}")
    
    def get_title(self):
        """Returns the page title."""
        return self.soup.title.string if self.soup.title else "No title found"
    
    def get_text(self):
        """Extracts and returns all text from the page."""
        return self.soup.get_text()
    
    def get_links(self):
        """Extracts and returns all links from the page."""
        return [a['href'] for a in self.soup.find_all('a', href=True)]
    
    def find_elements(self, tag: str, class_name: str = None):
        """Finds elements by tag and optional class name."""
        if class_name:
            return self.soup.find_all(tag, class_=class_name)
        return self.soup.find_all(tag)
    
    def find_by_selector(self, selector: str):
        """Finds elements using a CSS selector."""
        return self.soup.select(selector)
