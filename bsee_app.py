
import re
from whoosh_index import WhooshIndex
from flask import Flask, request


# load index
index = WhooshIndex('index_data', load=True)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def start():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Best Search Engine Ever - Start Page</title>
        <link rel="stylesheet" type="text/css" href="static/start.css">
        <link rel="stylesheet" type="text/css" href="static/form.css">
        <script src="static/search_suggestions.js"></script>
    </head>
    <body>
        <div id="content">
            <img id="logo" src="static/icon.png" alt="Best Search Engine Ever">
            <h1>Best Search Engine Ever</h1>
            <form action="search-results" method="get">
                <div>
                    <input id="search-input" type="text" autocomplete="off" name="q" placeholder="Enter your search">
                    <input type="submit" value="Search">
                    <div id="search-suggestions">
                        <div><ul id="search-suggestions-list"></ul></div>
                    </div>
                </div>
            </form>
        </div>
    </body>
    </html>
    '''


@app.route('/search-results', methods=['GET'])
def search_results():

    search_query = request.args.get('q', '')

    # search index using the search query
    search_results = index.search(search_query)

    # create list of search results
    if len(search_results) == 0:
        results_html = '<li>Oops such emptiness. Try a different search!</li>'
    else:
        results_html = ''.join(f'''
            <li style="background-color: rgb(26,{int(26+result['score']*26)},26)">
                <a href="{result['path']}" class="result-link">
                    <h2>{result['title']}</h2>
                    <cite>{' > '.join(['/'.join(result['path'].split('/')[:3]), *result['path'].split('/')[3:]])}</cite>
                </a>
                <p>{re.sub(r'class="match term[0-9]*"', 'class="highlight-match"', result['highlights'].replace('...', ' · '))}</p>
            </li>
        ''' for result in search_results)

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Best Search Engine Ever - Search Results</title>
        <link rel="stylesheet" type="text/css" href="static/results.css">
        <link rel="stylesheet" type="text/css" href="static/form.css">
        <script src="static/search_suggestions.js"></script>
    </head>
    <body>
        <div id="content">
            <div id="header">
                <a id="logo" href="."><img src="static/icon.png" alt="Best Search Engine Ever"></a>
                <h1>Best Search Engine Ever</h1>
                <form action="search-results" method="get">
                    <input id="search-input" type="text" autocomplete="off" name="q" placeholder="Enter your search" value="{search_query}">
                    <input type="submit" value="Search">
                    <div id="search-suggestions">
                        <div><ul id="search-suggestions-list"></ul></div>
                    </div>
                </form>
                <div id="result-ranking-info">
                    <div>
                        <p>What do the different shades of green mean?</p>
                        <p class="hidden">The different shades of green indicate how good the result matches your search query in relation to the other results. A brighter shade of green means a better match regarding the BM25 score.</p>
                    </div>
                </div>
            </div>
            <div id="results">
                <ul>
                    {results_html}
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''


@app.route("/search-suggestions", methods=['GET'])
def search_suggestions():

    search_query = request.args.get('q', '')

    # get search suggestions using the search query
    search_suggestions = index.suggest(search_query)

    return search_suggestions


if __name__ == "__main__":
    app.run(debug=False)
