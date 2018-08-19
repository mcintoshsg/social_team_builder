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

        user_data_2 = {
            'email': 'testuser2@test.com',
            'display_name': 'test user 2',
            'password': 'XGEyPfoMRNYTo7A#yWLnKEht',
            'bio': 'test bio 2',
            'avatar': '',
        }
        self.skill_1 = Skill.objects.create(skill_type='Python Developer')
        self.user_1 = User.objects.create(**user_data_1)
        self.user_1.set_password('XGEyPfoMRNYTo7A#yWLnKEht')
        self.user_1.save()

        self.user_2 = User.objects.create(**user_data_2)
        self.user_2.set_password('XGEyPfoMRNYTo7A#yWLnKEht')
        self.user_2.save()

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
        self.project_2 = Project.objects.create(**project_data_2)

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

        self.edit_project_data = {
            'name': 'Project 1',
            'description': 'This project got BIGGER',
            'requirements': 'Work long Hours',
            'timeline': '1000 hours',
            'owner': self.user_1,
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '',
            'form-MAX_NUM_FORMS': '',
            'form-0-skill': 'Python Developer',
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
        self.assertEqual(saved_project .count(), 2)
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
        # print(response.content)
        # self.assertEqual(response.status_code, 200)
        # response = self.client.get('/projects/all/')
        # self.assertContains(response, 'Bigger Project')

    def test_project_detail_view(self):
        self.login()
        response = self.client.get(reverse(
            'projects:detail',
            kwargs={'pk': self.project_1.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Big Project')
        self.assertTemplateUsed(response, 'projects/project_detail.html')

    def test_delete_project_get_view(self):
        self.login()
        response = self.client.get(reverse(
            'projects:delete',
            kwargs={'pk': self.project_2.id}
        ))
        self.assertContains(response,
                            'Are you sure you want to delete this project?'
                            )

    def test_delete_project_post_view(self):
        self.login()
        response = self.client.post(reverse(
            'projects:delete',
            kwargs={'pk': self.project_2.id}
        ), follow=True)

        self.assertRedirects(response,
                             reverse('projects:all'),
                             status_code=302)
        self.assertContains(response, 'Project successfully deleted')

    def test_edit_project_get_view(self):
        self.login()
        response = self.client.get(reverse(
            'projects:edit',
            kwargs={'pk': self.project_1.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Big Project')
        self.assertTemplateUsed(response, 'projects/edit_project.html')

    def test_edit_project_post_view(self):
        self.login()
        response = self.client.post(reverse(
            'projects:edit',
            kwargs={'pk': self.project_1.id}),
            self.edit_project_data, follow=True
        )
        # self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Big Project')
        # self.assertTemplateUsed(response, 'projects/edit_project.html')
        # print(response.content)

    def test_completed_project_view(self):
        self.login()
        response = self.client.post(reverse(
            'projects:completed',
            kwargs={'pk': self.project_1.id}
        ), follow=True)
        self.assertRedirects(response,
                             reverse('projects:all'),
                             status_code=302)
        completed_project = Project.objects.get(id=self.project_1.id)
        self.assertTrue(completed_project.completed, True)

    def test_search_project_view(self):
        self.login()
        response = self.client.get(
            '/projects/search/', {'search_projects': 'Small'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Small Project')
        self.assertTemplateUsed(response, 'projects/all_projects.html')

    def test_filter_project_view(self):
        response = self.client.get(reverse(
            'projects:filter',
            kwargs={'pk': self.skill_1.id}
        ))
        self.assertContains(response, 'Python Developer')

    def test_apply_view(self):
        self.client.login(email='testuser2@test.com',
                          password='XGEyPfoMRNYTo7A#yWLnKEht')
        response = self.client.get(reverse(
            'projects:apply',
            kwargs={'pk': self.position_1.id}
        ))
        applied = Applications.objects.filter(
            position=self.position_1.id)
        self.assertTrue(applied[0].applicant, self.user_2.id)
        self.assertContains(
            response, 'Your application for {} was posted'.format(
                self.position_1.skill
            )
        )

    def test_applications_view(self):
        self.login()
        response = self.client.get('/projects/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/applications.html')
        self.assertContains(response,
                            '<title>Applications | Social Teams</title>')

    def test_application_accept_view(self):
        self.client.login(email='testuser2@test.com',
                          password='XGEyPfoMRNYTo7A#yWLnKEht')
        response = self.client.get(reverse(
            'projects:accept',
            kwargs={
                'decision': 1,
                'pk': self.position_1.id,
                'id': self.user_2.id
            }
        ))
        accepted = Applications.objects.filter(
            position=self.position_1.id)

        self.assertTrue(accepted[0].status, 'Accepted')
        self.assertRedirects(response,
                             reverse('projects:applications'),
                             status_code=302)

    def test_add_skill_view(self):
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '',
            'form-MAX_NUM_FORMS': '',
            'form-0-skill_type': 'Angular Developer',
        }
        self.login()
        response = self.client.post(
            '/projects/add_skill/', data)
        skill = Skill.objects.get(skill_type='Angular Developer')
        self.assertEqual(skill.skill_type, 'Angular Developer')
        self.assertRedirects(response,
                             reverse('projects:new'),
                             status_code=302)
