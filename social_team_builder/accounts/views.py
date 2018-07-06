from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (FormView, RedirectView, CreateView,
                                  TemplateView)

from . forms import UserCreateForm
from . models import User
from projects.models import Project, UserSkill

import pdb

# class SignInView(FormView):
#     form_class = AuthenticationForm
#     template_name = "accounts/signin.html"

#     def get_form(self, form_class=None):
#         if form_class is None:
#             form_class = self.get_form_class()
#         return form_class(self.request, **self.get_form_kwargs())

#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return super().form_valid(form)

#     def get_success_url(self, **kwargs):
#         return reverse_lazy("accounts:profile",
#                             kwargs={'pk': self.request.user.id})


class SignOutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        ''' for each user porofile has the following attributes
            1. Who they are: display name, bio, avatar / photo
            completed projects

            2. Skills:  What skills do they have

            3. Projects: What project they are owners of and what are the
            projects they have  worked on i.e. completed.

            '''
        context = super().get_context_data(**kwargs)

        # get the user attributes to pass into the context - display anme etc..
        user = User.objects.get(id=kwargs['pk'])

        # get the users projects to pass into the context - where they were
        # the owner and wheer they have worked on a project that has completed
        owned_projects = Project.objects.filter(owner=user)
        worked_on_projects = Project.objects.filter(completed=True)
        worked_on_projects = worked_on_projects.filter(
                                    project_position__filled_by=user)

        # get the users skills
        user_skills = UserSkill.objects.filter(user=user)

        pdb.set_trace()
        roles = []
        for r in worked_on_projects:
            roles.append(r.project_position__role.skill_type) 

        # add all of the above to the context and return
        context['user'] = user
        context['owned_projects'] = owned_projects
        context['worked_on_projects'] = worked_on_projects
        context['user_skills'] = user_skills
        return context
