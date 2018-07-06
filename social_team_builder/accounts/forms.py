from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from . models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("display_name", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"


class EditProfileForm(forms.ModelForm):
    ''' form to allow changes to the User Profile '''
    bio = forms.CharField(max_length=300, 
                          min_length=10,
                          help_text='Use at least 10 characters.')

    class Meta:
        model = User
        fields = (
            'display_name',
            'bio',
            'avatar',
        )        