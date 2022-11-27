from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.PostRecruit)
admin.site.register(models.Recruit)
admin.site.register(models.GroupedSkillz)
admin.site.register(models.Skill)