# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from website_app.models import PostRecruit, Recruit
from asgiref.sync import sync_to_async

class PostRecruitPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        
        # If item class is not expected, send them to next pipeline
        if type(item).__name__ != 'PostRecruitItem':
            return item
        post_recruit = PostRecruit(
            post_id = item.get('post_id'),
            post_title = item.get('post_title'),
            post_slug = item.get('post_slug'),
            post_replies = item.get('post_replies'),
            post_created = item.get('post_created'),
            post_url = item.get('post_url'),
            post_toon_url = item.get('post_toon_url')
        )
        post_recruit.save()
        return item

class RecruitPipeline: 
    @sync_to_async
    def process_item(self, item, spider):

        # If item class is not expected, send them to next pipeline
        if type(item).__name__ != 'RecruitItem':
            return item

        post = item.get('post_recruit')

        recruit = Recruit(
            name = item.get('name'),
            character_id = item.get('character_id'),
            corporation = item.get('corporation'),
            date_of_birth = item.get('date_of_birth'),
            security_status = item.get('security_status'),
            alliance = item.get('alliance'),
            unallocated_sp = item.get('unallocated_sp'),
            total_sp = item.get('total_sp'),

            available_remaps = item.get('available_remaps'),
            charisma = item.get('charisma'),
            intelligence = item.get('intelligence'),
            memory = item.get('memory'),
            perception = item.get('perception'),
            willpower = item.get('willpower'),
            implant_slot1 = item.get('implant_slot1'),
            implant_slot2 = item.get('implant_slot2'),
            implant_slot3 = item.get('implant_slot3'),
            implant_slot4 = item.get('implant_slot4'),
            implant_slot5 = item.get('implant_slot5'),
            post_recruit = PostRecruit.objects.get(pk=post['post_id'])
        )
        recruit.save()
        return item