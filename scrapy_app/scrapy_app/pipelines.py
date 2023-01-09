# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from website_app.models import PostRecruit, Recruit, GroupedSkillz, Skill
from asgiref.sync import sync_to_async


class PostRecruitPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        # If item class is not expected, send them to next pipeline
        if type(item).__name__ != 'PostRecruitItem':
            return item

        post_recruit = PostRecruit(
            post_id=item.get('post_id'),
            post_title=item.get('post_title'),
            post_slug=item.get('post_slug'),
            post_replies=item.get('post_replies'),
            post_created=item.get('post_created'),
            post_last=item.get('post_last'),
            post_url=item.get('post_url'),
            post_toon_url=item.get('post_toon_url')
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

        # combine profile image url
        profile_img_url = f"https://images.evetech.net/characters/{item.get('character_id')}/portrait"

        recruit = Recruit(
            name=item.get('name'),
            character_id=item.get('character_id'),
            profile_img_url=profile_img_url,
            corporation=item.get('corporation'),
            date_of_birth=item.get('date_of_birth'),
            security_status=item.get('security_status'),
            alliance=item.get('alliance'),
            unallocated_sp=item.get('unallocated_sp'),
            total_sp=item.get('total_sp'),
            available_remaps=item.get('available_remaps'),
            charisma=item.get('charisma'),
            intelligence=item.get('intelligence'),
            memory=item.get('memory'),
            perception=item.get('perception'),
            willpower=item.get('willpower'),
            implant_slot1=item.get('implant_slot1'),
            implant_slot2=item.get('implant_slot2'),
            implant_slot3=item.get('implant_slot3'),
            implant_slot4=item.get('implant_slot4'),
            implant_slot5=item.get('implant_slot5'),
            post_toon_url=item.get('post_toon_url'),
            post_url=item.get('post_url'),
            post_recruit=PostRecruit.objects.get(pk=post['post_id'])
        )
        recruit.save()
        return item


class GroupedSkillzPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        if type(item).__name__ != 'GroupedSkillzItem':
            return item

        group_recruit = item.get('recruit')

        grouped_skillz = GroupedSkillz(
            grouped_skillz_id=item.get('grouped_skillz_id'),
            group_id=item.get('group_id'),
            group_name=item.get('group_name'),
            group_total_sp=item.get('group_total_sp'),
            recruit=Recruit.objects.get(pk=group_recruit['character_id'])
        )

        grouped_skillz.save()
        return item


class SkillPipeline:
    @sync_to_async
    def process_item(self, item, spider):

        if type(item).__name__ != 'SkillItem':
            return item

        skill = Skill(
            skill_id=item.get('skill_id'),
            skill_name=item.get('skill_name'),
            skill_rank=item.get('skill_rank'),
            skill_character_id=item.get('skill_character_id'),
            skill_group_id=item.get('skill_group_id'),
            skill_group_name=item.get('skill_group_name'),
            skill_active_level=item.get('skill_active_level'),
            skill_points_in_skill=item.get('skill_points_in_skill'),
            skill_trained_level=item.get('skill_trained_level'),

            grouped_skillz=GroupedSkillz.objects.get(pk=item.get('skill_character_id') + item.get('skill_group_id')),
            recruit=Recruit.objects.get(pk=item.get('skill_character_id'))
        )

        skill.save()
        return item
