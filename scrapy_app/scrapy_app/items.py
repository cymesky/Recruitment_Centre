# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from website_app.models import PostRecruit, Recruit, GroupedSkillz, Skill


class PostRecruitItem(DjangoItem):
    django_model = PostRecruit


class RecruitItem(DjangoItem):
    django_model = Recruit


class GroupedSkillzItem(DjangoItem):
    django_model = GroupedSkillz


class SkillItem(DjangoItem):
    django_model = Skill
