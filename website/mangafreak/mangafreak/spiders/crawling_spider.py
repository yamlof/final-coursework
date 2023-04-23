from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor


class MangafreakSpider(CrawlSpider):
    name = "latest_titles"
    allowed_domains = ["mangafreak.net"]
    start_urls = ["https://w15.mangafreak.net/"]

    rules = (
        Rule(LinkExtractor(allow="/Manga/")),
    )


    def parse_manga(self,response):
        yield{
            "cover" : response.css(".manga_series_image img::attr[src]").get(default='not found'),
            "title" : response.css(".manga_series_data h1::text").get(default='not found'),
            "autor_name" : response.css(".manga_series_data div::text").get(default='not found'),
            "manga_description" : response.css(".manga_series_description p::text").get(default='not found'),
            "chapter_number" : response.css(".manga_series_list_section"), 
        }

    





 
