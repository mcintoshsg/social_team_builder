from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


# from . models import User
from projects.models import UserSkill, Skill

import pdb

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('display_name', 'email', 'password1', 'password2')
        model = get_user_model()


class EditProfileForm(forms.ModelForm):
    ''' form to allow changes to the User Profile '''
    bio = forms.CharField(widget=forms.Textarea(
                        attrs={'placeholder': 'enter your bio...'}))   

    class Meta:
        model = get_user_model()
        fields = (
            'display_name',
            'bio',
            'avatar',
        )


class SkillForm(forms.ModelForm):
    ''' form to add in skills on the user profile '''
    # skill_type = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        # self.queryset = UserSkill.objects.filter(user=self.user)
        # pdb.set_trace()
        # if self.instance.skill.skill_type:
        #     self.fields['skill'].initial = self.instance.skill.skill_type
        super(SkillForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Skill
        fields = ('skill_type',)

    def clean(self):
        '''
        before we validate the skill we need to check 2 things
        1. if a new skill type has been added create a new record
        2. check that we have not already saved this skill
        '''
        # pdb.set_trace()
        data = self.cleaned_data['skill_type']
        skill, created = Skill.objects.get_or_create(skill_type=data)
        if not UserSkill.objects.filter(skill=skill.id,
                                        user=self.user).exists():
            UserSkill.objects.create(skill=skill, user=self.user)
        return


SkillFormSet = forms.modelformset_factory(
    Skill,
    form=SkillForm,
    extra=1,
)
