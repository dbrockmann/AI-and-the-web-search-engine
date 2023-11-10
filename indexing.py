
def build_index(html_contents):
    """
    Builds a simple dictionary based index with each word as the keys and a list of URLs that refer to pages including the word as values. Receives a dictionary with URLs as keys and HTML content as values.

    Args:
        html_contents: dictionary of URLs to HTML content

    Returns:
        dictionary of words to URLs which contain the word
    """

    index = dict()

    for url in html_contents:
        # ??
        for word in html_contents[url]:
            
            if word in index:
                index[word].append(url)
            else:
                index[word] = [url]
