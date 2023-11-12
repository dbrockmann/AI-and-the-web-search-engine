
import re
from bs4 import BeautifulSoup


class BasicIndex:
    """
    Builds a simple dictionary based index with words as the keys and a list of URLs that refer to pages including the word as values
    """

    def __init__(self):
        """
        Initialize empty index
        """

        self.index = dict()

    def add(self, url, html_content):
        """
        Adds content from an URL to the index. Receives an URL as keys and HTML content.

        Args:
            url: URL to the content
            html_content: HTML content
        """

        soup = BeautifulSoup(html_content, 'html.parser')
        for str in soup.find_all(text=True):

            for word in self.clean_str(str).split(' '):
            
                if word in self.index:
                    if not url in self.index[word]:
                        self.index[word].append(url)
                else:
                    self.index[word] = [url]

    def clean_str(self, str):
        """
        Clean a string by removing everything but letters and make them lowercase

        Args:
            str: string to clean

        Returns:
            cleaned string
        """

        str = re.sub(r'[^\w\s]', '', str)
        str = re.sub(r'\s{2,}', ' ', str)
        str = str.lower()

        return str
    
    def search(self, search_query):
        """
        Search for a word in the index and retrieve a list of page which include that word

        Args:
            search_query: word to search for

        Returns:
            list of URLs which include the search word
        """

        if search_query in self.index:
            return self.index[search_query]
        else:
            return []
