from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from projects import models


class Home(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("projects:all"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        '''
        1. List out all projects and skills irrespective of owner
        2. List out all project needs
        '''
        context = super().get_context_data(**kwargs)

        all_skills = []

        open_projects = models.Project.objects.filter(
                            completed=False
                            ).prefetch_related(
                            'position_set'
                            )
        for project in open_projects:
            for position in project.position_set.all():
                all_skills.append(position.skill)

        context['all_skills'] = all_skills
        context['skill_set'] = set(all_skills)
        context['open_projects'] = open_projects
        return context
