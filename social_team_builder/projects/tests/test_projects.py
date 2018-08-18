''' Tests for projects app '''
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from accounts.models import User
from ..models import UserSkill, Project, Skill, Position, Applications
from ..forms import (ProjectForm, PositionForm, PositionFormSet)


#################
# Base Setup
#################
class BaseTestCase(TestCase):
    '''SETUP '''

    def setUp(self):
        user_data_1 = {
            'email': 'testuser1@test.com',
            'display_name': 'test user 1',
            'password': 'XGEyPfoMRNYTo7A#yWLnKEht',
            'bio': 'test bio 1',
            'avatar': '',
        }
        self.skill_1 = Skill.objects.create(skill_type='Python Developer')
        self.user_1 = User.objects.create(**user_data_1)
        self.user_1.set_password('XGEyPfoMRNYTo7A#yWLnKEht')
        self.user_1.save()

        self.user_skills_1 = UserSkill.objects.create(
            skill=self.skill_1,
            user=self.user_1
        )
        project_data_1 = {
            'name': 'Project 1',
            'description': 'Big Project',
            'requirements': 'Work long Hours',
            'timeline': '1000 hours',
            'owner': self.user_1,
        }
        project_data_2 = {
            'name': 'Project 2',
            'description': 'Small Project',
            'requirements': 'New York',
            'timeline': '1 hours',
            'owner': self.user_1,
        }
        self.project_1 = Project.objects.create(**project_data_1)
        position_data = {
            'skill': self.skill_1,
            'project': self.project_1,
            'filled_by': self.user_1
        }
        self.position_1 = Position.objects.create(**position_data)
        application_data = {
            'position': self.position_1,
            'applicant': self.user_1,
            'status': 'Accepted'
        }
        self.application_1 = Applications.objects.create(**application_data)

        position_formset_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '',
            'form-MAX_NUM_FORMS': '',
            'form-0-skill': self.skill_1,
            'form-0-description': 'Develop backend'
        }

        self.project_post_data = {**project_data_2, **position_formset_data}

        self.client = Client()

    def login(self):
        self.client.login(email='testuser1@test.com',
                          password='XGEyPfoMRNYTo7A#yWLnKEht')


#################
# Test Models
#################
class SkillModelTest(BaseTestCase):
    ''' test out the skill model'''

    def test_saving_and_retrieving_skills(self):
        saved_skills = Skill.objects.all()
        self.assertEqual(saved_skills.count(), 1)
        self.assertEqual(saved_skills[0].skill_type, self.skill_1.skill_type)


class UserSkillModelTest(BaseTestCase):
    ''' test out the userskill model'''

    def test_saving_and_retrieving_userskills(self):
        saved_user_skills = UserSkill.objects.all()
        self.assertEqual(saved_user_skills .count(), 1)
        self.assertEqual(saved_user_skills[0].skill, self.skill_1)


class ProjectModelTest(BaseTestCase):
    ''' test out the project model'''

    def test_saving_and_retrieving_projects(self):
        saved_project = Project.objects.all()
        self.assertEqual(saved_project .count(), 1)
        self.assertEqual(saved_project[0].name, self.project_1.name)


class ApplicationsModelTest(BaseTestCase):
    ''' test out the applications model'''

    def test_saving_and_retrieving_applications(self):
        saved_application = Applications.objects.all()
        self.assertEqual(saved_application.count(), 1)
        self.assertEqual(saved_application[0].position,
                         self.position_1)


#####################
# Test Projects Views
#####################
class ProjectsViewTest(BaseTestCase):
    ''' test of our views '''

    def test_all_projects_view(self):
        self.login()
        response = self.client.get('/projects/all/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/all_projects.html')
        self.assertContains(response, self.project_1.name)

    def test_new_project_view(self):
        self.login()
        response = self.client.get('/projects/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/new_project.html')
        response = self.client.post(
            '/projects/new/',
            self.project_post_data
        )
        print(response.content)
        # self.assertEqual(response.status_code, 200)
        # response = self.client.get('/projects/all/')
        # self.assertContains(response, 'Bigger Project')


        
#     def test_sign_up_post_view(self):
#         response = self.client.post('/accounts/signup/', sign_up_data)
#         self.assertRedirects(response, '/accounts/login/')

#     def test_sign_out_view(self):
#         self.login()
#         response = self.client.post('/accounts/signout/')
#         self.assertRedirects(response, '/')

#     def test_profile_view(self):
#         self.login()
#         user = User.objects.get(email='testuser1@test.com')
#         response = self.client.get(reverse('accounts:profile',
#                                    kwargs={'pk': user.id}))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response,
#                             '<title>Profile | Test User 1</title')

#     def test_edit_profile_view(self):
#         self.login()
#         user = User.objects.get(email='testuser1@test.com')
#         response = self.client.get(reverse('accounts:edit',
#                                            kwargs={'pk': user.id}))
#         self.assertContains(
#             response,
#             '<title>Edit Profile | Test User 1</title>')

#         response = self.client.post(
#             reverse('accounts:edit',
#                     kwargs={'pk': user.id}),
#             edit_profile_data)

#         response = self.client.get(
#             reverse('accounts:profile',
#                     kwargs={'pk': user.id}))
#         self.assertContains(
#             response,
#             'test user 1, your profile was successfully updated')


# ##################
# # Test Forms
# ##################
# class AccountsFormTests(TestCase):
#     ''' test out all the forms '''

#     def test_UserCreateForm_valid(self):
#         form = UserCreateForm(data=sign_up_data)
#         self.assertTrue(form.is_valid())
#         self.assertTrue(form.cleaned_data['display_name'],
#                         'stuart mcintosh')

#     def test_UserCreateForm_not_valid(self):
#         form = UserCreateForm(data=sign_up_data_bad)
#         self.assertFalse(form.is_valid())
#         self.assertTrue({'password_mismatch':
#                          "The two password fields didn't match."},
#                         form.error_messages
#                         )

#     def test_EditProfileForm_valid(self):
#         form = EditProfileForm(data=edit_data)
#         self.assertTrue(form.is_valid())
#         self.assertTrue(form.cleaned_data['bio'],
#                         'Lorum Ipsum')

#     def test_EditProfileForm_not_valid(self):
#         form = EditProfileForm(data={})
#         self.assertFalse(form.is_valid())
#         self.assertEqual(form.errors['display_name'],
#                          ['This field is required.'])

#     def test_SkillForm_valid(self):
#         form = SkillForm(data=skill_data)
#         self.assertTrue(form.is_valid())
#         self.assertTrue(form.cleaned_data['skill_type'],
#                         'Django Developer')

#     def test_SkillFormSet_valid(self):
#         formset = SkillFormSet(data=skill_formset_data)
#         self.assertTrue(formset.is_valid())
#         self.assertTrue(formset.cleaned_data[0]['skill_type'],
#                         'Test')
