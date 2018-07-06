from django.contrib import admin

from . import models

admin.site.register(models.Project)
admin.site.register(models.Skill)
admin.site.register(models.UserSkill)
admin.site.register(models.ProjectPosition)
admin.site.register(models.ProjectApplication)

