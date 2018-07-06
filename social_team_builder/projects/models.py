from django.conf import settings
from django.db import models



class Skill(models.Model):
    skill_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.skill_type


class UserSkill(models.Model):
    skill = models.ForeignKey(Skill, related_name='user_skill',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='user',
                             on_delete=models.CASCADE)

    def __str__(self):
        return '{} / {}'.format(
            self.user.username,
            self.skill.skill_type
        )


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default='')
    timeline = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return '{} / {}'.format(
            self.name,
            self.description
        )


class ProjectPosition(models.Model):
    role = models.ForeignKey(Skill, related_name='skill')
    project = models.ForeignKey(Project, related_name='project_position')
    requirements = models.CharField(max_length=255, unique=False)
    is_filled = models.BooleanField(default=False)
    filled_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='filled_by', blank=True,
                                  null=True)

    def __str__(self):
        if self.filled_by:
            return "{} / {} / filled_by {}".format(
                self.project.name,
                self.role,
                self.filled_by.display_name
            )
        else:
            return "{} / {} / not filled".format(
                self.project.name,
                self.role
            )


class ProjectApplication(models.Model):
    position = models.ForeignKey(ProjectPosition,
                                 related_name='project_applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='applicant')

    class Meta:
        unique_together = ['position', 'applicant']

    def __str__(self):
        return "{} / applied for by {}".format(
            self.position,
            self.applicant
        )
