# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from website_app.models import PostRecruit


class ScrapyAppPipeline:
    def process_item(self, item, spider):
        recruit = PostRecruit(
            post_id = item.get('post_id'),
            post_title = item.get('post_title'),
            post_slug = item.get('post_slug'),
            post_replies = item.get('post_reply'),
            post_created = item.get('post_created'),
            post_url = item.get('post_url'),
            post_toon_url = item.get('toon_url')
        )
        recruit.save()
        return item
