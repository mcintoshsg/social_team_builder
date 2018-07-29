from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, CreateView, DeleteView,
                                  UpdateView, DetailView, RedirectView)  
from django.urls import reverse

from accounts.models import User
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
    context_object_name = 'open_projects'


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    model = models.Project
    success_url = reverse_lazy("projects:all")

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Project successfully deleted")
        return super().delete(*args, **kwargs)


class EditProjectView(LoginRequiredMixin, UpdateView):
    pass


class SearchProjectView(LoginRequiredMixin, ListView):
    template_name = 'projects/all_projects.html'
    model = models.Project
    # paginate_by = 1
    # may need to rethink this to get projects that are also completed
    # change the tempate context_object_name in the template
    context_object_name = 'open_projects'

    def get_queryset(self):
        '''
        search the projects models, name and description fields for a 
        query string sent in by the user. the reqults will only contain
        projects that a current
        '''
        search_criteria = self.request.GET.get('search_projects')
        results = models.Project.objects.filter(
            Q(name__icontains=search_criteria) |
            Q(description__icontains=search_criteria),
            completed=False,
            ).prefetch_related(
                            'position_set'
                            ).order_by('id')
        if results:
            return results
        return messages.success(self.request,
                                'No projects matched your search!')


class FilterProjectView(LoginRequiredMixin, ListView):
    '''
    Holding off implementin this view as I am unsure its erquired
    '''
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
    def get(self, request, *args, **kwargs):
        '''Accepts or regjects the applicants and sends a confirmation email
        Arguments:
            pk = Position being applied for
            id = of the applicant
            decsion = accepted or rejected
        Returns:
            Redirects back to the applications page
        '''
        user = get_object_or_404(User, id=self.kwargs['id'])
        position = get_object_or_404(models.Position, id=self.kwargs['pk'])
        if int(self.kwargs['decision']) == 1 and position.is_filled is False:
            position.filled_by = user
            position.is_filled = True
            position.save()
            position.refresh_from_db()

            # not sure about the code below - refactor
            for application in position.applications_set.all():
                if application.applicant == position.filled_by:
                    application.status = 'Accepted'
                    self.send_response(position, application.applicant,
                                       'Accepted')
                else:
                    application.status = 'Rejected'
                    self.send_response(position, application.applicant,
                                       'Rejected')
            application.save()                           
        else:
            applicant = models.Applications.objects.get(position=position,
                                                        applicant=user)
            applicant.status = 'Rejected'
            applicant.save()
            self.send_response(position, applicant.applicant, 'Rejected')
        return super(ApplicationAcceptView, self).get(request, *args, **kwargs)

    @staticmethod
    def send_response(position, applicant, status):
        user = get_object_or_404(User, username=applicant)
        subject = '{}'.format(position.skill.skill_type)
        message = 'Your application for the position above has been {}'.format(
            status
        )
        from_email = 'admin@social_teams.com'
        to_email = user.email
        if subject and message and from_email:
            send_mail(subject, message, from_email, [to_email])
        else:
            print('error with email')
        return

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projects:applications')
