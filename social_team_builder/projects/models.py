from django.conf import settings
from django.db import models


class Skill(models.Model):
    skill_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.skill_type


class UserSkill(models.Model):
    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE,
                              related_name='skill')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='user')

    def __str__(self):
        return '{} / {}'.format(
            self.user.username,
            self.skill.skill_type
        )

    class Meta:
        unique_together = ['skill', 'user']


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default='')
    requirements = models.CharField(max_length=30, null=True)
    timeline = models.CharField(max_length=30, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return '{} / {}'.format(
            self.name,
            self.owner.display_name
        )

    class Meta:
        ordering = ['id']


class Position(models.Model):
    skill = models.ForeignKey(Skill)
    project = models.ForeignKey(Project)
    description = models.TextField(blank=True, default='')
    is_filled = models.BooleanField(default=False)
    filled_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='filled_by', blank=True,
                                  null=True)

    def __str__(self):
        if self.filled_by:
            return "{} / {} / filled_by {}".format(
                self.project.name,
                self.skill,
                self.filled_by.display_name
            )
        else:
            return "{} / {} ".format(
                self.project.name,
                self.skill
            )
   

class Applications(models.Model):
    position = models.ForeignKey(Position)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.CharField(max_length=30, default='Pending')

    class Meta:
        unique_together = ['position', 'applicant']
        verbose_name_plural = 'Applications'

    def __str__(self):
        return "{} / applied for by {} application in {}".format(
            self.position,
            self.applicant,
            self.status
        )
