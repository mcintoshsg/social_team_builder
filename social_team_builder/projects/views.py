from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (ListView, CreateView, DeleteView,
                                  UpdateView, DetailView)  
from django.urls import reverse

from . import forms
from . import models

import pdb

class AllProjectsView(LoginRequiredMixin, ListView):
    '''
    List out all the projects - login in is required as you can apply for 
    a project on the page. Overide the quesryset to only pass in the projects
    that are not completed
    '''
    template_name = 'projects/all_projects.html'
    model = models.Project
    # paginate_by = 1
    context_object_name = 'open_projects'

    def get_query_set(self):
        ''' get the queryset to use in the template '''
        return models.Project.objects.filter(
                            completed=False
                            ).prefetch_related(
                            'position_set'
                            ).order_by(id)


class NewProjectView(LoginRequiredMixin, CreateView):
    '''
    View to create a new project - overide get context to pass in data 
    depending on the requestself.
    Also override form valid so we can update the models and capture any new
    positions created dynamically on the page
    '''
    model = models.Project
    template_name = 'projects/new_project.html'
    form_class = forms.ProjectForm

    def get_context_data(self, **kwargs):
        # get any data already associated with the context
        context = super(NewProjectView, self).get_context_data(**kwargs)
        pdb.set_trace()
        if self.request.POST:
            context['position_form'] = forms.PositionFormSet(self.request.POST)
        else:
            context['position_form'] = forms.PositionFormSet()
        return context

    def form_valid(self, form):
        # get the positions from the context
        context = self.get_context_data()
        pdb.set_trace()
        positions = context['position_form']
        if form.is_valid():
            form = form.save(commit=False)
            # add the current user as the project owner
            form.owner = self.request.user
            form.save()
        if positions.is_valid():
            project = models.Project.objects.last()
            # iterate through all the newly created positions and add
            # the associated project
            for position in positions:
                # make changes before committing ot the database
                position = position.save(commit=False)
                # associate the newly created project
                position.project = project
                position.save()
            # And notify our users that it worked
            messages.success(self.request,
                             '{} Project created successfully'.format(
                              project.name
                              ))
        return super(NewProjectView, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:all')


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = models.Project
    template = 'projects/project_detail.html'
    context_object_name = 'project'


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    pass


class EditProjectView(LoginRequiredMixin, UpdateView):
    pass


class ApplyView(AllProjectsView):
    '''
    Current user has applied for a role in a project
    Update the application Model with the position and user
    then send message confirming application
    '''

    def get(self, request, *args, **kwargs):
        ''' create the new application '''
        position = models.Position.objects.get(pk=self.kwargs['pk'])
        # check if the user has already applied
        application, created = models.Applications.objects.get_or_create(
                                        position=position,
                                        applicant=self.request.user)
        if created:
            messages.success(self.request,
                             'Your application for {} was posted'.format
                             (position.skill))
        else:
            messages.success(self.request,
                             'You have already applied for this position')

        # get the object list to send back
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


class ApplicationsView(LoginRequiredMixin, ListView):
    '''
    This controller lists out the following:
    1. status of all of a current users applications to projects
    2. list of all applicants for current users projects
    3  list of all current users projects
    4. list of all current users project positions

    The view has the following capabilities:
    1. allow the current user to accept or reject application of their project
    '''
    template_name = 'projects/applications.html'
    model = models.Applications
    context_object_name = 'applications'

    def get_context_data(self, **kwargs):
        # get any data already associated with the context
        context = super(ApplicationsView, self).get_context_data(**kwargs)
        owned_projects = models.Project.objects.filter(owner=self.request.user)

        # get all positions for user projects
        try:
            positions = owned_projects.get().position_set.all()
        except ObjectDoesNotExist:
            context['positions'] = None
        else:
            context['positions'] = positions

        # update the context
        context['user'] = self.request.user
        context['owned_projects'] = owned_projects
        return context
