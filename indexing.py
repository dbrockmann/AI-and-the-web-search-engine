
class Index:
    """
    Builds a simple dictionary based index with each word as the keys and a list of URLs that refer to pages including the word as values
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

        for word in html_content:
            
            if word in self.index:
                self.index[word].append(url)
            else:
                self.index[word] = [url]
