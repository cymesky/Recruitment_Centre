import json

import scrapy
from scrapy_splash import SplashRequest
from website_app.models import PostRecruit

from ..items import PostRecruitItem, RecruitItem, GroupedSkillzItem, SkillItem


class EveCrawlerSpider(scrapy.Spider):
    name = 'eve_crawler'

    # load database post_id list
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.posts_ids_in_db = list(x[0] for x in PostRecruit.objects.values_list('post_id'))

    def start_requests(self):
        url = 'https://forums.eveonline.com/c/marketplace/character-bazaar/60/l/latest.json?ascending=false&page=0'

        number_of_pages = 15

        for page_number in range(0, number_of_pages):
            page_url = url + str(page_number)

            yield SplashRequest(page_url, callback=self.parse_page, args={
                'wait': 1
            })

    def parse_page(self, response):
        rejected_words = ('WTB', 'PRIVATE SALE', 'PRIVATE-SALE',
                          'SOLD', 'CLOSE', 'REMOVE', 'NEW SKILLBOARD')

        response_without_html_tags = response.css('pre::text').extract_first()
        jsonresponse = json.loads(response_without_html_tags)
        topics = jsonresponse.get('topic_list')['topics']

        t_range = len(topics)

        for i in range(0, t_range):

            # if post exist in database, skipping
            if topics[i]['id'] in self.posts_ids_in_db:
                continue

            post = PostRecruitItem()
            post['post_id'] = topics[i]['id']
            post['post_title'] = topics[i]['title']

            # if post contains rejected words, skipping
            if any(pst in post['post_title'].upper() for pst in rejected_words):
                continue

            post['post_slug'] = topics[i]['slug']
            post['post_replies'] = topics[i]['reply_count']
            post['post_created'] = topics[i]['created_at'][0:10]
            post['post_last'] = topics[i]['last_posted_at'][0:10]
            post['post_url'] = f"https://forums.eveonline.com/t/{post['post_slug']}/{post['post_id']}"

            yield SplashRequest(post['post_url'], callback=self.parse_post, args={'wait': 1},
                                meta={'post_item': post})

    def parse_post(self, response):
        post = response.meta.get('post_item')

        # Parsing recruit url #
        slug_for_toon_url = response.css('a[href*="skillboard.eveisesi.space/users/"]::attr(href)').extract_first()

        if slug_for_toon_url is not None:
            slug_for_toon_url = f'https://api.{slug_for_toon_url[8:]}'

            if slug_for_toon_url[-1] == '/':
                slug_for_toon_url = slug_for_toon_url[:-1]
            elif slug_for_toon_url[-2:] == '/#':
                slug_for_toon_url = slug_for_toon_url[:-2]

            post['post_toon_url'] = slug_for_toon_url
        else:
            post['post_toon_url'] = response.css(
                'a[href*="skillq.net/char/"]::attr(href)').extract_first()

        # Checking is recruit url existed and is from eveisesi page only
        if post['post_toon_url'] is None:
            return None
        elif 'char' in post['post_toon_url']:
            return None
        elif 'users' in post['post_toon_url']:
            yield SplashRequest(post['post_toon_url'], callback=self.parse_recruit, meta={'post_item': post})

    def parse_recruit(self, response):
        post = response.meta.get('post_item')

        recruit = RecruitItem()

        data = json.loads(response.css('pre::text').extract_first())

        # Check is recruit exist #
        name = data.get('character')

        # If not break parsing
        if name is None:
            return None

        recruit['name'] = name.get('name')
        # Recruit name was found then add post to database #
        yield post

        # Check is alliance exist #
        alliance = data.get('character').get('corporation').get('alliance')

        if alliance is not None:
            recruit['alliance'] = alliance.get('name')
        else:
            recruit['alliance'] = ''

            # Check is available remaps exist #
        available_remaps = data.get('attributes').get('bonus_remaps')

        if available_remaps is not None:
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

        if implants is not None:
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

        # parsing unallocated_sp
        unallocated_sp = data.get('meta').get('unallocated_sp')
        if unallocated_sp is not None:
            recruit['unallocated_sp'] = data['meta']['unallocated_sp']
        else:
            recruit['unallocated_sp'] = 0

        # parsing always present recruit elements
        recruit['character_id'] = data['character_id']
        recruit['corporation'] = data['character']['corporation']['name']
        recruit['date_of_birth'] = data['character']['birthday'][:10]
        recruit['security_status'] = data['character']['security_status']
        recruit['total_sp'] = data['meta']['total_sp']
        recruit['charisma'] = data['attributes']['charisma']
        recruit['intelligence'] = data['attributes']['intelligence']
        recruit['memory'] = data['attributes']['memory']
        recruit['perception'] = data['attributes']['perception']
        recruit['willpower'] = data['attributes']['willpower']
        recruit['post_recruit'] = post

        # send recruit to RecruitPipeline
        yield recruit

        # parsing grouped skillz
        grouped_skills = data.get('groupedSkillz')
        number_of_grouped_skills = len(grouped_skills)

        if grouped_skills is not None:
            for g in range(number_of_grouped_skills):

                grouped_skillz = GroupedSkillzItem()
                grouped_skillz['group_id'] = grouped_skills[g].get('group_id')
                grouped_skillz['group_name'] = grouped_skills[g].get('group_name')
                grouped_skillz['group_total_sp'] = grouped_skills[g].get('total_group_sp')
                grouped_skillz['grouped_skillz_id'] = recruit['character_id'] + grouped_skillz['group_id']
                grouped_skillz['recruit'] = recruit

                yield grouped_skillz

                # parsing skills
                skills = grouped_skills[g].get('skills')
                number_of_skills = len(skills)

                for s in range(number_of_skills):
                    # if character_id is not exist then this skill is not injected
                    if skills[s].get('character_id') is None:
                        continue

                    skill = SkillItem()
                    skill['skill_id'] = skills[s].get('id')
                    skill['skill_name'] = skills[s].get('name')
                    skill['skill_rank'] = skills[s].get('skill_rank')
                    skill['skill_character_id'] = skills[s].get('character_id')
                    skill['skill_group_id'] = skills[s].get('group_id')
                    skill['skill_group_name'] = skills[s].get('group_name')
                    skill['skill_active_level'] = skills[s].get('active_skill_level')
                    skill['skill_points_in_skill'] = skills[s].get('skillpoints_in_skill')
                    skill['skill_trained_level'] = skills[s].get('trained_skill_level')

                    yield skill
