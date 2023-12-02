
import sys
import re
import numpy as np
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin
from whoosh.scoring import BM25F
from whoosh.index import EmptyIndexError
from bs4 import BeautifulSoup
from bs4.element import Comment


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
            title = TEXT(stored=True),
            content = TEXT(stored=True)
        )

        if not load:
            self.index = index.create_in(folder_path, schema)
        else:
            try:
                self.index = index.open_dir(folder_path)
            except EmptyIndexError:
                sys.exit('Error: Build the index before starting the web app.')


    def add(self, url, html_content):
        """
        Adds content from an URL to the index. Receives an URL and HTML content.

        Args:
            url: URL to the content
            html_content: HTML content
        """

        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.find('title').string

        content = soup.find_all(text=True)
        content = filter(lambda x: not x.parent.name in ['[document]', 'head', 'meta', 'script', 'style', 'title'], content)
        content = filter(lambda x: not isinstance(x, Comment), content)
        content = ' '.join(content)
        content = content.replace('\n', ' ')
        content = re.sub(r'\s+', ' ', content.strip())

        writer = self.index.writer()
        writer.add_document(path=url, title=title, content=content)
        writer.commit()

    def suggest(self, search_query):
        """
        Give word suggestions for a given search query. Note: only affects the last word of the query

        Args:
            search_query: basis of suggestion

        Returns:
            list of word suggestions
        """

        if len(search_query) == 0:
            return []

        pre_string = ' '.join([*search_query.split()[:-1], ''])
        last_word = search_query.split()[-1]

        with self.index.searcher() as searcher:
            corrector = searcher.corrector('content')
            suggestions = corrector.suggest(last_word, limit=5)

        suggestions = [pre_string + s for s in suggestions]

        return suggestions

    def search(self, search_query):
        """
        Search the index using a search query and retrieve a list of pages

        Args:
            search_query: query to search for

        Returns:
            list of dictionaries with path and title
        """

        query_parser = MultifieldParser(['title', 'content'], schema=self.index.schema)
        query_parser.add_plugin(FuzzyTermPlugin())

        fuzzy_search_query = ' '.join(f'{word}~1' for word in search_query.split())
        parsed_query = query_parser.parse(fuzzy_search_query)

        with self.index.searcher(weighting=BM25F()) as searcher:
            results = searcher.search(parsed_query, limit=10, terms=True)
            results.fragmenter.maxchars = 100
            results.fragmenter.surround = 40

            # normalize scores using min-max normalization
            scores = np.array([result.score for result in results])
            normalized_scores = np.nan_to_num((scores-np.min(scores))/(np.max(scores)-np.min(scores)), nan=1.0) if len(scores) > 1 else np.full(len(scores), 1.0)

            result_dicts = [
                {
                    'path': result['path'],
                    'title': result['title'],
                    'score': normalized_score,
                    'highlights': result.highlights('content', top=3)
                } for result, normalized_score in zip(results, normalized_scores)
            ]

        return result_dicts
