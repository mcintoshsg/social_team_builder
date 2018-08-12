from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import (ListView, CreateView, DeleteView,
                                  UpdateView, DetailView, RedirectView)
from django.urls import reverse

from accounts.models import User
from accounts.forms import SkillFormSet
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
    paginate_by = 1
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
        # skill_form is passed to be used in the modal to add a new skill
        context['skill_form'] = SkillFormSet(
            queryset=models.Skill.objects.none()
        )
        return context

    def form_valid(self, form, **kwargs):
        context = self.get_context_data()
        positions = context['position_form']
        if form.is_valid() and positions.is_valid():
            form = form.save(commit=False)
            form.owner = self.request.user
            form.save()
            project = models.Project.objects.last()
            for position in positions:
                position = position.save(commit=False)
                position.project = project
                position.save()
            messages.success(self.request,
                             '{} Project created successfully'.format(
                                 project.name
                             ))
        else:
            context = {'form': form, 'position_form': positions}
            return render(self.request, self.template_name, context)
        return super(NewProjectView, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:all')


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = models.Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project_detail'


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    model = models.Project
    success_url = reverse_lazy('projects:all')

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Project successfully deleted")
        return super().delete(*args, **kwargs)


class EditProjectView(LoginRequiredMixin, UpdateView):
    '''
     Allow editing of the current project
    '''
    model = models.Project
    template_name = 'projects/edit_project.html'
    form_class = forms.ProjectForm

    def get_context_data(self, **kwargs):
        context = super(EditProjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['position_form'] = forms.PositionFormSet(
                data=self.request.POST)
        else:
            queryset = self.object.position_set.all()
            context['position_form'] = forms.PositionFormSet(queryset=queryset)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        positions = context['position_form']
        if form.is_valid() and positions.is_valid():
            form = form.save(commit=False)
            form.owner = self.request.user
            form.save()
            for position in positions:
                # if this is a change in on a current position - update
                # else the position is new so we need to create
                if position.cleaned_data:
                    skill = position.cleaned_data['skill']
                    description = position.cleaned_data['description']
                    if position.cleaned_data['id']is not None:
                        pos = models.Position.objects.get(
                            id=position.cleaned_data['id'].id)
                        pos.skill = skill
                        pos.description = description
                        pos.save()
                    else:
                        models.Position.objects.create(
                            skill=skill,
                            description=description,
                            project=self.object)
        else:
            context = {'form': form, 'position_form': positions}
            return render(self.request, self.template_name, context)
        messages.success(self.request,
                         '{} project updated successfully'.format(
                             self.object
                         ))
        return super(EditProjectView, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:all')


class CompletedProjectView(LoginRequiredMixin, RedirectView):
    ''' set the project to completed '''

    def get(self, request, *args, **kwargs):
        ''' update the project with completed and send an email to all
            people working on the project
        '''
        __sent_applicant = None
        project = get_object_or_404(models.Project, id=self.kwargs['pk'])
        project.completed = True
        project.save()
        # get all the positions and applicants of those positions
        positions = project.position_set.all().prefetch_related(
            'applications_set'
        )
        for position in positions:
            for applicant in position.applications_set.all():
                if applicant and applicant.applicant.email != __sent_applicant:
                    self.send_notification(project, applicant)
                    __sent_applicant = applicant.applicant.email
        messages.success(
            self.request,
            "Completed Project notifications have been sent successfully")
        return super(CompletedProjectView, self).get(request, *args, **kwargs)

    @staticmethod
    def send_notification(project, applicant):
        subject = '{}'.format(project.name)
        message = ''' Dear {}\n
                      The project {} has been successfully completed
                      thanks for all your hard work
                      \n\nRegards,
                      {}'''.format(applicant.applicant.display_name,
                                   project.name,
                                   project.owner)
        from_email = '{}'.format(project.owner)
        to_email = applicant.applicant.email
        if subject and message and from_email:
            send_mail(subject, message, from_email, [to_email])
        else:
            print('error with email')
        return

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projects:all')


class SearchProjectView(ListView):
    template_name = 'projects/all_projects.html'
    model = models.Project
    paginate_by = 1
    context_object_name = 'open_projects'

    def get_queryset(self):
        '''
        search the projects models, name and description fields for a
        query string sent in by the user. the reqults will only contain
        projects that a current
        '''
        search_criteria = self.request.GET.get('search_projects')
        if search_criteria != '':
            results = models.Project.objects.filter(
                Q(name__icontains=search_criteria) |
                Q(description__icontains=search_criteria),
                completed=False,
            ).prefetch_related(
                'position_set'
            ).order_by('id')
            if results:
                return results
            else:
                messages.info(self.request,
                              'No projects matched your search!')
        else:
            messages.warning(self.request,
                             'Please enter search criteria!')
        return models.Project.objects.all()


class FilterProjectView(ListView):
    '''
    Filter projects based on skills required
    '''
    template_name = 'projects/all_projects.html'
    model = models.Project
    paginate_by = 1
    context_object_name = 'open_projects'

    def get_queryset(self):
        '''
        search the projects models, for skills that match the id sent int
        the reqults will only contain projects that a current
        '''
        filter_id = self.kwargs['pk']
        results = models.Project.objects.filter(
            position__skill=filter_id,
            completed=False
        )

        if results:
            return results
        return messages.info(self.request,
                             'No projects matched your filter!')


class ApplyView(AllProjectsView):
    '''
    Current user has applied for a role in a project
    Update the application Model with the position and user
    then send message confirming application
    '''

    def get(self, request, *args, **kwargs):
        ''' create the new application '''
        position = models.Position.objects.get(pk=self.kwargs['pk'])
        application, created = models.Applications.objects.get_or_create(
            position=position,
            applicant=self.request.user)
        if created:
            messages.success(self.request,
                             'Your application for {} was posted'.format
                             (position.skill))
        else:
            messages.info(self.request,
                          'You have already applied for this position')
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return render(request, self.template_name, context)


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
        all_skills = set()
        owned_projects = models.Project.objects.filter(
            owner=self.request.user
        ).prefetch_related(
            'position_set', 'position_set__skill',
        )
        for project in owned_projects:
            for position in project.position_set.all():
                all_skills.add(position.skill)

        context['user'] = self.request.user
        context['skill_set'] = all_skills
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


class AddSkillView(LoginRequiredMixin, RedirectView):
    ''' Provides the ability to add in a new skill, must be unique!
        this view is called via a modal included in the new_project tempalate
        the context for the modal is passed to the new_project template
        via the NewProjectView
    '''

    def post(self, request, *args, **kwargs):
        formset = SkillFormSet(self.request.POST)
        if formset.is_valid():
            for form in formset:
                skill = form.cleaned_data['skill_type']
                obj, created = models.Skill.objects.get_or_create(
                    skill_type=skill
                )
                if created:
                    messages.success(
                        self.request,
                        '{} position has been created!'.format(obj.skill_type))
        else:
            # this is ugly - refactor!
            messages.info(self.request, '{} position already exists!'.format(
                formset[0]['skill_type'].value()))
        return super(AddSkillView, self).post(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projects:new')
