from django.contrib import admin

from . import models


class PositionInline(admin.StackedInline):
    model = models.Position


class ProjectAdmin(admin.ModelAdmin):
    inlines = [PositionInline, ]


# class ApplicationInline(admin.StackedInline):
#     model = models.Applicant


# class ProjectAdmin(admin.ModelAdmin):
#     inlines = [PositionInline, ]


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Skill)
admin.site.register(models.UserSkill)
admin.site.register(models.Applications)
