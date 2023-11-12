
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from bs4 import BeautifulSoup


class WhooshIndex:

    def __init__(self, folder_path, load=False):
        """
        Initializes new index or loads existing index

        Params:
            folder_path: path to the folder where the index should be/is stored
            load: whether to load an existing index or create a new one
        """

        schema = Schema(
            path = ID(stored=True),
            content = TEXT(stored=True)
        )

        if not load:
            self.index = index.create_in(folder_path, schema)
        else:
            self.index = index.open_dir(folder_path)

    def add(self, url, html_content):
        """
        Adds content from an URL to the index. Receives an URL and HTML content.

        Args:
            url: URL to the content
            html_content: HTML content
        """

        soup = BeautifulSoup(html_content, 'html.parser')
        content = soup.find_all(text=True)
        content = ' '.join(content)

        writer = self.index.writer()
        writer.add_document(path=url, content=content)
        writer.commit()

    def search(self, search_query):
        """
        Search the index using a search query and retrieve a list of pages

        Args:
            search_query: word to search for

        Returns:
            list of URLs
        """

        query_parser = QueryParser('content', schema=self.index.schema)
        parsed_query = query_parser.parse(search_query)

        with self.index.searcher() as searcher:
            results = searcher.search(parsed_query, limit=10)
            results_paths = [document['path'] for document in results]

        return results_paths
