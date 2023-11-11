from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def start():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Start Page</title>
        <link rel="stylesheet" type="text/css" href="/static/style.css"> <!-- Link to your CSS file -->
    </head>
    <body>
        <h1>Best search engine ever</h1>
        <form action="/search-results" method="post">
            <input type="text" name="input_text" placeholder="Enter your text here">
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    '''


@app.route("/search-results", methods=['POST'])
def search_results():
    input_text = request.form['input_text']
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Results</title>
        <link rel="stylesheet" type="text/css" href="/static/style.css">
    </head>
    <body>
        <h2>Best search engine ever - Search Results</h2>
        <div class="content">
            <p>Your results for the search: "{input_text}" are:</p>
            <!-- Here you can add logic to display actual search results -->
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(debug=True)
