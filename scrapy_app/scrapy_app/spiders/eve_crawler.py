import scrapy
from scrapy_splash import SplashRequest
from scrapy_app.items import PostRecruitItem

class EveCrawlerSpider(scrapy.Spider):
    name = 'eve_crawler'
    
    NUMBER_OF_PAGES = 1

    def start_requests(self):
        url = 'https://forums.eveonline.com/c/marketplace/character-bazaar/60/l/latest.json?ascending=false&page=0'
        return SplashRequest(url=url, callback=self.parse)


    def parse(self, response):
        
        NUMBER_OF_PAGES = 1

        for page_number in range(0, NUMBER_OF_PAGES):
            page_url = self.start_urls[0] + str(page_number)

            print(f"Page url: {page_url}")

            yield SplashRequest(page_url, callback=self.parse_page)

    
    def parse_page(self, response):

        REJECTED_WORDS = ('WTB', 'PRIVATE SALE', 'PRIVATE-SALE',
                          'SOLD', 'CLOSE', 'REMOVE', 'NEW SKILLBOARD')

        jsonresponse = response.json()
        topics = jsonresponse.get('topic_list')['topics']

        t_range = len(topics)

        for i in range(0, t_range):
            post = PostRecruitItem()

            post['post_id'] = topics[i]['id']
            post['post_title'] = topics[i]['title']

            if any(pst in post['post_title'].upper() for pst in REJECTED_WORDS):
                continue

            post['post_slug'] = topics[i]['slug']
            post['post_reply'] = topics[i]['reply_count']
            post['post_created'] = topics[i]['created_at']
            post['post_url'] = f"https://forums.eveonline.com/t/{post['post_slug']}/{post['post_id']}"

            yield scrapy.Request(post['post_url'], callback=self.parse_post, meta={'post_item': post})

    def parse_post(self, response):
        post = response.meta.get('post_item')
        post['toon_url'] = response.css(
            'a[href*="skillboard.eveisesi"]::attr(href)').extract_first()

        if post['toon_url'] == None:
            post['toon_url'] = response.css(
                'a[href*="skillq.net/"]::attr(href)').extract_first()

        yield post