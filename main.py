
from webcrawler import BasicCrawler
from indexing import Index


start_url = 'https://vm009.rz.uos.de/crawl/index.html'

index = Index()
crawler = BasicCrawler(start_url, index)
crawler.crawl()

while True:
    search_query = input('Enter search term: ')
    result = index.search(search_query)
    print(result)
