import requests
from bs4 import BeautifulSoup
from ct.abstracts import AbstractWebParser
from ct.interfaces import IProcessor

__All__ = ['WebParser']


class WebParser(AbstractWebParser):

    def fetch_content(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text

    def extract_text(self, raw_content: str) -> str:
        soup = BeautifulSoup(raw_content, 'html.parser')
        return soup.get_text()
