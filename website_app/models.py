from django.db import models

# Create your models here.
class PostRecruit(models.Model):
    post_id = models.IntegerField(primary_key=True, editable=False)
    post_title = models.CharField(max_length=255)
    post_slug = models.CharField(max_length=512)
    post_replies = models.CharField(max_length=255)
    post_created = models.CharField(max_length=512)
    post_url = models.CharField(max_length=512)
    post_toon_url = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.post_title


class Recruit(models.Model):
    name = models.CharField(max_length=512)
    character_id = models.IntegerField(primary_key=True, editable=False)
    corporation = models.CharField(max_length=512)
    date_of_birth = models.DateField()
    security_status = models.CharField(max_length=512)
    alliance = models.CharField(max_length=512)
    unallocated_sp = models.CharField(max_length=512)
    total_sp = models.CharField(max_length=512)
    available_remaps = models.CharField(max_length=512)
    charisma = models.CharField(max_length=512)
    intelligence = models.CharField(max_length=512)
    memory = models.CharField(max_length=512)
    perception = models.CharField(max_length=512)
    willpower = models.CharField(max_length=512)

    implant_slot1 = models.CharField(max_length=512)
    implant_slot2 = models.CharField(max_length=512)
    implant_slot3 = models.CharField(max_length=512)
    implant_slot4 = models.CharField(max_length=512)
    implant_slot5 = models.CharField(max_length=512)

    post_recruit = models.OneToOneField(PostRecruit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
