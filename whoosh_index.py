
import os
import sys
import re
import numpy as np
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin, OrGroup
from whoosh.scoring import BM25F
from whoosh.spelling import Corrector, ListCorrector
from whoosh.index import EmptyIndexError
from bs4 import BeautifulSoup
from bs4.element import Comment


class CustomMultiCorrector(Corrector):
    """
    Fix a bug in the MultiCorrector implementation, returning (sug, score) tuples insted of (score, sug) which is expected by Corrector. Issue on that bug exists since 2022 (https://github.com/mchaput/whoosh/issues/21).
    Add weighting for different correctors.
    Add automatic prefix for word suggestions.
    """

    def __init__(self, correctors, weighting):
        self.correctors = correctors
        self.weighting = weighting
    
    def _suggestions(self, text, maxdist, prefix):
        if prefix == 'auto':
            prefix = len(text)
        suggestions = {}

        for weight, corrector in zip(self.weighting, self.correctors):
            for score, sug in corrector._suggestions(text, maxdist, prefix):
                if not sug in suggestions:
                    suggestions[sug] = 0
                suggestions[sug] += weight * score

        for sug, score in suggestions.items():
            yield score, sug


class WhooshIndex:

    def __init__(self, folder_path, load=False, word_list='data/words_alpha.txt'):
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
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            self.index = index.create_in(folder_path, schema)
        else:
            try:
                self.index = index.open_dir(folder_path)
            except EmptyIndexError:
                sys.exit('Error: Build the index before starting the web app.')

        if not word_list is None:
            with open('data/words_alpha.txt', 'r') as word_file:
                word_data = word_file.read().split('\n')
                self.list_corrector = ListCorrector(word_data)


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
            search_corrector = searcher.corrector('content')
            corrector = CustomMultiCorrector([self.list_corrector, search_corrector], [1, 0.1])

            suggestions = corrector.suggest(last_word.lower(), limit=6, maxdist=6, prefix='auto')

        suggestions = [pre_string + last_word + s[len(last_word):] for s in suggestions]

        return suggestions

    def search(self, search_query):
        """
        Search the index using a search query and retrieve a list of pages

        Args:
            search_query: query to search for

        Returns:
            list of dictionaries with path and title
        """

        query_parser = MultifieldParser(['title', 'content'], schema=self.index.schema, group=OrGroup)
        query_parser.add_plugin(FuzzyTermPlugin())

        # fuzzy search query, longer prefix for shorter words
        fuzzy_search_query = ' '.join(f'{word}~2/2' if len(word) > 1 and len(word) < 5 else f'{word}~2/1' if len(word) < 7 else f'{word}~2' for word in search_query.split())
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
