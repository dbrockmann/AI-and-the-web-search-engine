from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def start():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Start Page</title>
        <link rel="stylesheet" type="text/css" href="/static/start.css"> <!-- Link to your CSS file -->
    </head>
    <body>
        <h1>Best search engine ever</h1>
        <form action="/search-results" method="get">
            <input type="text" name="q" placeholder="Enter your search">
            <input type="submit" value="Search">
        </form>
    </body>
    </html>
    '''


@app.route("/search-results", methods=['GET'])
def search_results():

    search_query = request.args.get('q', '')  

    # Eine vordefinierte Liste
    fitting_urls = ["Element 1", "Element 2", "Element 3"]

    # Erstellen der HTML-Liste
    list_html = ''.join(f'<li>{item}</li>' for item in fitting_urls)


    return f'''
    
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Results</title>
        <link rel="stylesheet" type="text/css" href="/static/result.css">
    </head>
    <body>
        <h1>Best search engine ever - Search Results</h1>
        <div>
            <p>Your results for the search: "{search_query}" are:</p>
            <ul>
                {list_html}
            </ul>
            <!-- Additional logic for displaying actual search results can be added here -->
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(debug=True)
