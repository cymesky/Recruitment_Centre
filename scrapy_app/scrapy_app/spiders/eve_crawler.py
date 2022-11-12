import scrapy


class EveCrawlerSpider(scrapy.Spider):
    name = 'eve_crawler'
    allowed_domains = ['forums.eveonline.com']
    start_urls = ['https://forums.eveonline.com/c/marketplace/character-bazaar/60']

    def parse(self, response):
        pass
