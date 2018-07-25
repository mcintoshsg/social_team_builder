from django.contrib.auth import logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (RedirectView, CreateView, UpdateView,
                                  DetailView)
from django.urls import reverse

from . import forms
from . models import User
from projects import models


import pdb

class SignOutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = forms.UserCreateForm
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


class EditProfileView(LoginRequiredMixin, UpdateView):
    '''
     Allow editing of the current user profile
    '''
    model = User
    template_name = 'accounts/edit_profile.html'
    form_class = forms.EditProfileForm

    def get_context_data(self, **kwargs):
        '''
         for each user profile has the following attributes
        1. Who they are: display name, bio, avatar / photo  completed projects
        2. Skills:  What skills do they have
        3. Projects: What project they are owners of and what are the
        projects they have  worked on i.e. completed.
        '''
        # get any data already associated with the context
        context = super(EditProfileView, self).get_context_data(**kwargs)
        # pass in the skillformset so as to allow users to add new skills
        if self.request.POST:
            context['skill_form'] = forms.SkillFormSet(
                                self.request.POST,
                                form_kwargs={'user': self.request.user})
        else:
            user_skills = models.Skill.objects.filter(
                                            skill__user=self.request.user)
            context['skill_form'] = forms.SkillFormSet(
                                                    queryset=user_skills)

        # get the users projects to pass into the context - where they were
        # the owner and where they have worked on a project that has completed
        owned_projects = models.Project.objects.filter(owner=self.request.user)
        worked_on_projects = models.Project.objects.filter(
                                        completed=True,
                                        position__filled_by=self.request.user
                                        )
        # get all worked on projects(user has fileld a position),
        # prefecth all the positions
        try:
            positions = worked_on_projects.get().position_set.filter(
                                                filled_by=self.request.user
                                                )
        except ObjectDoesNotExist:
            context['positions'] = None
        else:
            context['positions'] = positions

        # get the users skills
        user_skills = models.UserSkill.objects.filter(user=self.request.user)
        context['user'] = self.request.user
        context['owned_projects'] = owned_projects
        context['worked_on_projects'] = worked_on_projects
        context['user_skills'] = user_skills
        return context

    def form_valid(self, form):
        '''
        check the forms are valid
        for the skills, check if the skill already exists, if then add it as
        as well as to the user skill set
        '''
        context = self.get_context_data()
        skill_forms = context['skill_form']
        if form.is_valid():
            form = form.save(commit=False)
            form.avatar = self.request.FILES
            form.save()
        if skill_forms.is_valid():
            for skill_form in skill_forms:
                skill_form.save()
            # And notify our users that it worked
            messages.success(
                        self.request,
                        '{}, your profile was successfully updated'.format(
                         self.request.user.display_name
                        ))
        else:
            # add in a more robust set of fail conditions
            print(skill_forms.errors)
        return super(EditProfileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('accounts:profile',
                       kwargs={'pk': self.request.user.id})
