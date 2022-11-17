import scrapy
import json
from scrapy_splash import SplashRequest
from scrapy_app.items import PostRecruitItem, RecruitItem
import scrapy_app.settings as settings
class EveCrawlerSpider(scrapy.Spider):
    name = 'eve_crawler'

    def start_requests(self):    
        url = 'https://forums.eveonline.com/c/marketplace/character-bazaar/60/l/latest.json?ascending=false&page=0'

        NUMBER_OF_PAGES = 1

        for page_number in range(0, NUMBER_OF_PAGES):
            page_url = url + str(page_number)

            yield SplashRequest(page_url, callback=self.parse_page, args={
                'wait': 2
            })

    
    def parse_page(self, response):
        REJECTED_WORDS = ('WTB', 'PRIVATE SALE', 'PRIVATE-SALE',
                          'SOLD', 'CLOSE', 'REMOVE', 'NEW SKILLBOARD')

        response_without_html_tags = response.css('pre::text').extract_first()
        jsonresponse = json.loads(response_without_html_tags)
        topics = jsonresponse.get('topic_list')['topics']

        t_range = len(topics)
        
        for i in range(0, t_range):
            post = PostRecruitItem()

            post['post_id'] = topics[i]['id']
            post['post_title'] = topics[i]['title']

            if any(pst in post['post_title'].upper() for pst in REJECTED_WORDS):
                continue

            post['post_slug'] = topics[i]['slug']
            post['post_replies'] = topics[i]['reply_count']
            post['post_created'] = topics[i]['created_at']
            post['post_url'] = f"https://forums.eveonline.com/t/{post['post_slug']}/{post['post_id']}"

            yield SplashRequest(post['post_url'], callback=self.parse_post, args={'wait': 2}, meta={'post_item': post})
                        

    def parse_post(self, response):
        post = response.meta.get('post_item')

        # Parsing recruit url #
        slug_for_toon_url = response.css('a[href*="skillboard.eveisesi.space/users/"]::attr(href)').extract_first()               

        if slug_for_toon_url != None:
            slug_for_toon_url = f'https://api.{slug_for_toon_url[8:]}'  

            if slug_for_toon_url[-1] == '/':
                slug_for_toon_url = slug_for_toon_url[:-1]        

            post['post_toon_url'] = slug_for_toon_url
        else:
            post['post_toon_url'] = response.css(
                'a[href*="skillq.net/char/"]::attr(href)').extract_first()

        if post['post_toon_url'] == None:
            return None
        elif 'char' in post['post_toon_url']:
            yield post
        elif 'users' in post['post_toon_url']:
            yield SplashRequest(post['post_toon_url'], callback=self.parse_recruit, meta={'post_item': post})
    
    def parse_recruit(self, response):
        post = response.meta.get('post_item')
        recruit = RecruitItem()

        data = json.loads(response.css('pre::text').extract_first())

        # Check is recruit exist #
        name = data.get('character')

        if name != None:
            recruit['name'] = name.get('name')
        else:
            print ("Parsing problem")
            print (f"Post { post['post_url'] } skipped")
            return None
             
        # Recruit name was finded then add post to database #
        yield post

        # Check is alliance exist #
        alliance = data.get('character').get('corporation').get('alliance')

        if alliance != None:
            recruit['alliance'] = alliance.get('name')
        else:
            recruit['alliance'] = ''   

        # Check is avaiable remaps exist #
        available_remaps = data.get('attributes').get('bonus_remaps')
        
        if available_remaps != None:
            recruit['available_remaps'] = available_remaps
        else:
            recruit['available_remaps'] = '0'

        # Parsing implants #

        implants = data.get('implants')
        implant_slot1 = ''
        implant_slot2 = ''
        implant_slot3 = ''
        implant_slot4 = ''
        implant_slot5 = ''


        if implants != None:
            for i in implants:
                if i.get('slot') == 1:
                    implant_slot1 = i.get('implant_name')
                elif i.get('slot') == 2:
                    implant_slot2 = i.get('implant_name')
                elif i.get('slot') == 3:
                    implant_slot3 = i.get('implant_name')
                elif i.get('slot') == 4:
                    implant_slot4 = i.get('implant_name')
                elif i.get('slot') == 5:
                    implant_slot5 = i.get('implant_name')

        recruit['implant_slot1'] = implant_slot1 
        recruit['implant_slot2'] = implant_slot2
        recruit['implant_slot3'] = implant_slot3
        recruit['implant_slot4'] = implant_slot4
        recruit['implant_slot5'] = implant_slot5

        recruit['character_id'] = data['character_id']
        recruit['corporation'] = data['character']['corporation']['name']
        recruit['date_of_birth'] = data['character']['birthday'][:10]
        recruit['security_status'] = data['character']['security_status']
        recruit['unallocated_sp'] = data['meta']['unallocated_sp']
        recruit['total_sp'] = data['meta']['total_sp']
        recruit['charisma'] = data['attributes']['charisma']
        recruit['intelligence'] = data['attributes']['intelligence']
        recruit['memory'] = data['attributes']['memory']
        recruit['perception'] = data['attributes']['perception'] 
        recruit['willpower'] = data['attributes']['willpower']

        recruit['post_recruit'] = post


        yield recruit

