''' Tests for accounts app '''
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from ..models import User
from ..forms import (UserCreateForm, SkillForm, EditProfileForm,
                     SkillFormSet)

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

sign_up_data = {
    'email': 's.g.mcintosh@test.com',
    'display_name': 'stuart mcintosh',
    'password1': 'XGEyPfoMRNYTo7A#yWLnKEht',
    'password2': 'XGEyPfoMRNYTo7A#yWLnKEht',
}

sign_up_data_bad = {
    'email': 's.g.mcintosh@test.com',
    'display_name': 'stuart mcintosh',
    'password1': 'XGEyPfoMRNYTo7A#yWLnKEht',
    'password2': '#yWLnKEht',
}


edit_data = {
    'display_name': 'stuart mcintosh',
    'bio': 'Lorum Ipsum'
}

skill_data = {
    'skill_type': 'Django Developer'
}

skill_formset_data = {
    'form-TOTAL_FORMS': '1',
    'form-INITIAL_FORMS': '0',
    'form-MIN_NUM_FORMS': '',
    'form-MAX_NUM_FORMS': '',
    'form-0-skill_type': 'Test',
}

edit_profile_data = {
    'display_name': 'stuart mcintosh',
    'bio': 'Lorum Ipsum',
    'form-TOTAL_FORMS': '1',
    'form-INITIAL_FORMS': '0',
    'form-MIN_NUM_FORMS': '',
    'form-MAX_NUM_FORMS': '',
    'form-0-skill_type': 'Test',
}


#################
# Test User Model
#################
class UserModelTest(TestCase):
    ''' test out the user model'''

    def setUp(self):
        self.user1 = User.objects.create(**user_data_1)
        self.user2 = User.objects.create(**user_data_2)

    def test_saving_and_retrieving_users(self):
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 2)
        self.assertEqual(saved_users[0].bio, 'test bio 1')
        self.assertEqual(saved_users[1].username, '@testuser2')


#####################
# Test Accounts Views
#####################
class AccountsViewsTest(TestCase):
    ''' test of our views '''

    def setUp(self):
        self.user1 = User.objects.create(**user_data_1)
        self.user1.set_password('XGEyPfoMRNYTo7A#yWLnKEht')
        self.user1.save()

        self.client = Client()

    def login(self):
        self.client.login(email='testuser1@test.com',
                          password='XGEyPfoMRNYTo7A#yWLnKEht')

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_sign_up_view(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_sign_up_post_view(self):
        response = self.client.post('/accounts/signup/', sign_up_data)
        self.assertRedirects(response, '/accounts/login/')

    def test_sign_out_view(self):
        self.login()
        response = self.client.post('/accounts/signout/')
        self.assertRedirects(response, '/')

    def test_profile_view(self):
        self.login()
        user = User.objects.get(email='testuser1@test.com')
        response = self.client.get(reverse('accounts:profile',
                                   kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            '<title>Profile | Test User 1</title')

    def test_edit_profile_view(self):
        self.login()
        user = User.objects.get(email='testuser1@test.com')
        response = self.client.get(reverse('accounts:edit',
                                           kwargs={'pk': user.id}))
        self.assertContains(
            response,
            '<title>Edit Profile | Test User 1</title>')

        response = self.client.post(
            reverse('accounts:edit',
                    kwargs={'pk': user.id}),
            edit_profile_data)

        response = self.client.get(
            reverse('accounts:profile',
                    kwargs={'pk': user.id}))
        self.assertContains(
            response,
            'test user 1, your profile was successfully updated')


##################
# Test Forms
##################
class AccountsFormTests(TestCase):
    ''' test out all the forms '''

    def test_user_create_form_valid(self):
        form = UserCreateForm(data=sign_up_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['display_name'],
                        'stuart mcintosh')

    def test_user_create_form_not_valid(self):
        form = UserCreateForm(data=sign_up_data_bad)
        self.assertFalse(form.is_valid())
        self.assertTrue({'password_mismatch': 
                         "The two password fields didn't match."},
                        form.error_messages
                        )

    def test_edit_profile_form_valid(self):
        form = EditProfileForm(data=edit_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['bio'],
                        'Lorum Ipsum')

    def test_edit_profile_form_not_valid(self):
        form = EditProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['display_name'],
                         ['This field is required.'])

    def test_skill_form_valid(self):
        form = SkillForm(data=skill_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['skill_type'],
                        'Django Developer')

    def test_skill_form_set_valid(self):
        formset = SkillFormSet(data=skill_formset_data)
        self.assertTrue(formset.is_valid())
        self.assertTrue(formset.cleaned_data[0]['skill_type'],
                        'Test')
