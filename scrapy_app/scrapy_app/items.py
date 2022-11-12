# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from website_app.models import PostRecruit, Recruit, Skill


class ScrapyAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PostRecruitItem(DjangoItem):
    django_model = PostRecruit

class RecruitItem(DjangoItem):
    django_model = Recruit

class SkillItem(DjangoItem):
    django_model = Skill