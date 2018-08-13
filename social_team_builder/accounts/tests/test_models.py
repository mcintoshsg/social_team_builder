from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from .models import User

user_data_1 = {
    'email': 'testuser1@test.com',
    'display_name' 'test user 1'
    'username': 'testuser 1',
    'password': 'XGEyPfoMRNYTo7A#yWLnKEht',
    'bio': 'test bio 1',
    'avatar': '',
}

user_data_2 = {
    'email': 'testuser2@test.com',
    'display_name' 'test user 2'
    'username': 'testuser2',
    'password': 'XGEyPfoMRNYTo7A#yWLnKEht',
    'bio': 'test bio 2',
    'avatar': '',
}

# test modles
class UserProfileModelTest(TestCase):
    ''' test out the user model'''
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(**user_data)
        )

    def test_saving_and_retrieving_users(self):
        saved_users = UserProfile.objects.all()
        self.assertEqual(saved_users.count(), 1)
        self.assertEqual(saved_users[0].bio, 'this is my life')
