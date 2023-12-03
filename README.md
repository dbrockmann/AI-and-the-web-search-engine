
# AI and the Web - Search Engine

Search engine project of the course AI and the Web at the University of Osnabrück.

## Features

- dynamic search suggestions while typing based on a word list and crawled content
- fuzzy search to find content despite typos
- search result preview with marked search query matches
- color indication of the results to show how good a result matches the search

### Crawler

The crawler crawls all pages on a server by following links starting on a base URL. HTML pages are parsed to find all reachable pages without leaving the base URL. The crawler keeps track of all visited pages to not visit pages multiple times or run into loops.

### Index

While crawling, a `Whoosh` index is built containing the information of all pages that were found by extracting text contents and titles. Additionally, the resulting text is filtered to only include text that is visible for a visiting user and additional spaces and line breaks are removed.

### Suggestions

While typing, suggestions for possible words that start with the typed letters are shown to the user. These suggestions are based on two sources, a) an english word list and b) the content of the crawled pages. The given `Correctors` for these suggestions are combined in a custom class to fix an existing bug in the `Whoosh` implementation and introduce an additional weight. The content of the crawled pages is given more weight than the word list, which means that suggestions are more likely to be based on real content.

### Searching

For searching the index, both title and contents of the pages are searched for matches. To be able to find more matches when entering multiple words, the default `AND` grouping is changed to `OR`. Additionally, we use a fuzzy search which allows up to 2 'mistakes' in each word to find content despite typos. The required prefix that has to match varies by word length to get better results. The search uses the BM25 weighting to order the results and additionally returns previews of the results that contain parts of the search query.

### App

The app is implemented using `Flask`. It includes a start page, from which a search can be started and a page with results of a previous search. The results are colored in a varying shade of green which is based on the normalized search scores. If for example the first 3 results match the search query equally good, they have the same color. This can enhance the user experience as it gives information about the results in addition to the order. In addition to the title and URL of a result, the list includes a preview of parts that include the search query. These words are also marked as matches. To enhance the search experience, the app shows search suggestions which are constantly updated while typing. This feature is implemented by using a `javascript` script that sends a `GET` request to the server each time the search text is altered. The response is the put in a list which is shown under the search bar. A click on a suggestion opens the results page for that search.

## Getting Started

Install the requirements included in [requirements.txt](requirements.txt).
```
pip install -r requirements.txt
```

Start the crawler and build the index (change the starting URL in [build_index.py](build_index.py)).
```
python build_index.py
```

Start the `Flask` app and open the app in your browser. You can also use the [bsee.wsgi](bsee.wsgi) file.
```
python bsee_app.py
```
