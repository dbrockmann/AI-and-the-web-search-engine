
from webcrawler import BasicCrawler
from basic_index import BasicIndex
from whoosh_index import WhooshIndex


start_url = 'https://vm009.rz.uos.de/crawl/index.html'

#index = BasicIndex()
index = WhooshIndex('index_data')
crawler = BasicCrawler(start_url, index)
crawler.crawl()
