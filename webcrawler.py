import requests
from bs4 import BeautifulSoup

class BasicCrawler:
    def __init__(self, base_url, index):
        # Remove any trailing slashes and store the base URL
        self.base_url = base_url.rstrip('/')
        print(self.base_url)
        # Extract the domain name to ensure we stay on the same server
        self.domain = self.get_domain(self.base_url)
        print("domain", self.domain)
        # Keep a set of URLs that we have already visited
        self.visited_urls = set()
        # Start with a set that includes only the base URL
        self.urls_to_visit = {self.base_url}
        # Index to store information
        self.index = index

    def get_domain(self, url):
        # Get the domain of a URL by stripping away the 'http://' or 'https://'
        # and any paths or page references after the domain name
        return url.split("//")[-1].split("/")[0]

    def crawl(self):
        # Keep crawling until we have no more URLs left to visit
        print(self.urls_to_visit)
        while self.urls_to_visit:
            url = self.urls_to_visit.pop()
            if url not in self.visited_urls:
                self.visit_url(url)

    def visit_url(self, url):
        # Log the URL we are about to crawl
        print(f"Crawling: {url}")
        try:
            # Perform an HTTP GET request to fetch the content at the URL
            response = requests.get(url, headers={'User-Agent': 'Custom Web Crawler'})
            # Check if the response is successful and is of type HTML
            if (response.status_code == 200 and
                    'text/html' in response.headers.get('Content-Type', '')):
                # Add URL to the visited set
                self.visited_urls.add(url)
                # Add information to index
                self.index.add(url, response.text)
                # Extract and queue new URLs found on this page
                self.extract_urls(response.text, url)
                print(self.extract_urls(response.text, url))
            else:
                # If the content is not HTML or the request failed, log the status code
                print(f"Failed to retrieve HTML content. Status code: {response.status_code}")
        except requests.RequestException as e:
            # If an HTTP request exception occurs, print the error
            print(f"An error occurred while visiting {url}: {e}")

    def extract_urls(self, html_content, base_url):
        # Parse the HTML using BeautifulSoup to find all hyperlinks
        soup = BeautifulSoup(html_content, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            print("Überprüfende Links", href)
            # Make sure the URL is valid and within the same domain
            if self.is_valid_url(href):
                # Normalize the URL (handle relative paths)
                full_url = self.clean_url(base_url, href)
                # If we haven't already visited this URL, add it to the queue
                if full_url not in self.visited_urls:
                    self.urls_to_visit.add(full_url)

    
    def is_valid_url(self, href):
        # Check if the link is on the same domain, is a relative URL, and is not a fragment or query
        if href.startswith('#'):
            # Exclude fragment identifiers
            return False
        if href.startswith('http://') or href.startswith('https://'):
            # Absolute URL: Check if it's on the same domain
            return self.get_domain(href) == self.domain
        # If not an absolute URL with http/https, it's a relative URL
        return True


    """
    def clean_url(self, base, path):
        # Remove the fragment and return a full URL (handles relative paths as well)
        if path.startswith('http'):
            full_url = path.split('#')[0]  # Remove URL fragment
        else:
            full_url = f"{self.base_url}{path.split('#')[0]}"

        print("clean_url",full_url)
        return full_url

    """

    def clean_url(self, base, path):
        # Remove the fragment and return a full URL (handles relative paths as well)
        if path.startswith('http'):
            # If the path is an absolute URL, just remove the fragment
            full_url = path.split('#')[0]  # Remove URL fragment
        else:
            # Handle relative URLs
            # If the path does not start with '/', add it
            if not path.startswith('/'):
                path = '/' + path
            
            """
            The following part is because the base URL is not vm009.rz.uos.de but vm009.rz.uos.de/crawl/
            """

            # Split the URL by slashes
            url_parts = self.base_url.split('/')
            # Take the first four parts (scheme, domain, and the first path)
            base_path_url_parts = url_parts[:4]
            # Join these parts back with slashes
            base_path_url = '/'.join(base_path_url_parts)
    
            # Combine base URL with the relative path
            full_url = f"{base_path_url}{path.split('#')[0]}"

        print("clean_url", full_url)
        return full_url


# Instantiate the crawler with the starting URL
start_url = 'https://vm009.rz.uos.de/crawl/index.html'
crawler = BasicCrawler(start_url)
# Begin the crawling process
crawler.crawl()
