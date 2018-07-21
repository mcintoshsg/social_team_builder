from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (RedirectView, CreateView, DetailView)

from . forms import UserCreateForm
from . models import User
from projects import models


class SignOutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class ProfileView(LoginRequiredMixin, DetailView):
    '''
    get the detail for the request user profile
    this could be different the current authnicated user as we are allowing
    all users to review but not update another users profile
    '''
    model = User
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        '''
        for each user profile has the following attributes
        1. Who they are: display name, bio, avatar / photo  completed projects
        2. Skills:  What skills do they have
        3. Projects: What project they are owners of and what are the
        projects they have  worked on i.e. completed.
        '''
        context = super(ProfileView, self).get_context_data(**kwargs)
        # get the user attributes to pass into the context - display anme etc..
        # the user could be different the currently autenticated user
        profile_user = kwargs['object']

        # get the users projects to pass into the context - where they were
        # the owner and where they have worked on a project that has completed
        owned_projects = models.Project.objects.filter(owner=profile_user)
        worked_on_projects = models.Project.objects.filter(
                                            completed=True,
                                            position__filled_by=profile_user
                                            )
        # get all worked on projects(user has fileld a position),
        # prefecth all the positions
        try:
            positions = worked_on_projects.get().position_set.filter(
                                                filled_by=profile_user
                                                )
        except ObjectDoesNotExist:
            context['positions'] = None
        else:
            context['positions'] = positions

        # get the users skills
        user_skills = models.UserSkill.objects.filter(user=profile_user)
        context['user'] = self.request.user
        context['profile_user'] = profile_user
        context['owned_projects'] = owned_projects
        context['worked_on_projects'] = worked_on_projects
        context['user_skills'] = user_skills
        return context
