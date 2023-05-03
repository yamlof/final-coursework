from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from urllib.request import urlopen ,Request



class MangafreakSpider(CrawlSpider):
    name = "latest_titles"
    allowed_domains = ["mangafreak.net"]
    start_urls = ["https://w15.mangafreak.net/"]

    rules = [
        Rule(LinkExtractor(
            allow=['.*']),
             callback='parse_manga',
             follow=True)
        ]
    
    def parse_manga(self,response):

        yield{
            "cover" : response.css(".manga_series_image img::attr(src)").extract(),
            "title" : response.css(".manga_series_data h1::text").extract(),
            "autor_name" : response.css(".manga_series_data div::text").extract(),
            "manga_description" : response.css(".manga_series_description p::text").extract(),
            "chapter_number" : response.css(".manga_series_list_section"), 
        }

    





 
