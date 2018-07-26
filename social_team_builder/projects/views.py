from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, CreateView, DeleteView,
                                  UpdateView, DetailView, RedirectView)  

from django.urls import reverse
# from braces.views import PrefetchRelatedMixin

from . import forms
from . import models


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

    def get_queryset(self):
        ''' get the queryset to use in the template '''
        return models.Project.objects.filter(
                            completed=False
                            ).prefetch_related(
                            'position_set'
                            ).order_by('id')


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
        context = super(NewProjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['position_form'] = forms.PositionFormSet(
                                                data=self.request.POST)
        else:
            context['position_form'] = forms.PositionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        positions = context['position_form']
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = self.request.user
            form.save()
        if positions.is_valid():
            project = models.Project.objects.last()
            # iterate through all the newly created positions and add
            # the associated project
            for position in positions:
                position = position.save(commit=False)
                position.project = project
                position.save()
            messages.success(self.request,
                             '{} Project created successfully'.format(
                              project.name
                              ))
        else:
            # add in a more robust set of fail conditions
            print(positions.errors)                
        return super(NewProjectView, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:all')


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = models.Project
    template = 'projects/project_detail.html'
    context_object_name = 'project'


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    model = models.Project
    success_url = reverse_lazy("projects:all")

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Project successfully deleted")
        return super().delete(*args, **kwargs)


class EditProjectView(LoginRequiredMixin, UpdateView):
    pass


class SearchProjectView(LoginRequiredMixin, ListView):
    pass


class FilterPorjectView(LoginRequiredMixin, ListView):
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
    1. status of all of a current users applications to other projects
    2. list of all applicants for current users projects
    3  list of all current users projects
    4. list of all current users project positions

    The view has the following capabilities:
    1. allow the current user to accept or reject application of their project
    '''
    template_name = 'projects/applications.html'
    model = models.Applications
    context_object_name = 'applications'

    def get_queryset(self):
        return models.Applications.objects.filter(
                                        applicant=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ApplicationsView, self).get_context_data(**kwargs)
        owned_projects = models.Project.objects.filter(
                                                owner=self.request.user
                                                ).prefetch_related(
                                                    'position_set'
                                                )
        context['user'] = self.request.user
        context['owned_projects'] = owned_projects
        return context


class ApplicationAcceptView(LoginRequiredMixin, RedirectView):
    '''
        controller to accept position applications
    '''
    def get_object(self):
        return get_object_or_404(
            models.Community,
            slug=self.kwargs.get("slug")
        )

    def get_redirect_url(self, *args, **kwargs):
        return self.get_object().get_absolute_url()

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(models.User, username=self.kwargs['applicant'])
        position = get_object_or_404(models.Poistion,  id=self.kwargs['pk'])
        position.filled_by = user
        position.is_filled = True
        position.save()

        return super().get(request, *args, **kwargs)
