from django.db import models

# Create your models here.
class PostRecruit(models.Model):
    post_id = models.CharField(max_length=255)
    post_title = models.CharField(max_length=255)
    post_slug = models.CharField(max_length=512)
    post_replies = models.CharField(max_length=255)
    post_created = models.CharField(max_length=512)
    post_url = models.CharField(max_length=512)
    post_toon_url = models.CharField(max_length=512, blank=True, null=True)


class Recruit(models.Model):
    name = models.CharField(max_length=512)
    skills = models.CharField(max_length=512)
    corporation = models.CharField(max_length=512)
    date_of_birth = models.CharField(max_length=512)
    security_status = models.CharField(max_length=512)
    allocated_sp = models.CharField(max_length=512)
    alliance = models.CharField(max_length=512)
    unallocated_sp = models.CharField(max_length=512)
    total_sp = models.CharField(max_length=512)

    available_remaps = models.CharField(max_length=512)
    charisma = models.CharField(max_length=512)
    intelligence = models.CharField(max_length=512)
    memory = models.CharField(max_length=512)
    perception = models.CharField(max_length=512)
    willpower = models.CharField(max_length=512)

    post_recruit = models.ForeignKey(PostRecruit, on_delete=models.CASCADE)


class Skill(models.Model):

    skill_name = models.CharField(max_length=512)
    skill_group = models.CharField(max_length=512)
    skill_rank = models.CharField(max_length=512)
    skill_level = models.CharField(max_length=512)
    skill_total_sp = models.CharField(max_length=512)
    skill_max_sp = models.CharField(max_length=512)

    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)