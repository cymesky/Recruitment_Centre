from rest_framework import serializers
from .models import PostRecruit, Recruit, GroupedSkillz, Skill


class PostRecruitSerializer(serializers.HyperlinkedModelSerializer):
    recruit = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='recruit-detail')

    class Meta:
        model = PostRecruit
        fields = ['post_id', 'post_title', 'post_slug',
                  'post_replies', 'post_created', 'post_last',
                  'post_url', 'post_toon_url', 'recruit']


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_id', 'skill_name', 'skill_rank', 'skill_character_id',
                  'skill_group_id', 'skill_group_name', 'skill_active_level',
                  'skill_points_in_skill', 'skill_trained_level', 'grouped_skillz',
                  'recruit']


class GroupedSkillzSerializer(serializers.HyperlinkedModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = GroupedSkillz
        fields = ['grouped_skillz_id', 'group_id', 'group_name',
                  'group_total_sp', 'recruit', 'skills']


class RecruitSerializer(serializers.HyperlinkedModelSerializer):
    groupedskillzs = GroupedSkillzSerializer(many=True)
    # skills = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='skill-detail')

    class Meta:
        model = Recruit
        fields = ['name', 'character_id', 'profile_img_url', 'corporation',
                  'date_of_birth', 'security_status', 'alliance', 'unallocated_sp',
                  'total_sp', 'available_remaps', 'charisma', 'intelligence',
                  'memory', 'perception', 'willpower', 'implant_slot1',
                  'implant_slot2', 'implant_slot3', 'implant_slot4', 'implant_slot5',
                  'post_recruit', 'groupedskillzs', 'post_toon_url', 'post_url']


class AllSkillsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_name']
