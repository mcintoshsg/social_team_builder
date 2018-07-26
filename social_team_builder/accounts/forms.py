from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


# from . models import User
from projects.models import UserSkill, Skill


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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SkillForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Skill
        fields = ('skill_type',)

    def save(self):
        '''
        before we save the skill we need to check 2 things
        1. if a new skill has been added create it in the UserSkill model
        2. if a skill has  been changed/updated reflectn that in the US model
        '''
        if self.changed_data:
            super(SkillForm, self).save(self)
            try:
                # retrieve the newly created or changed ob
                skill = Skill.objects.get(
                    skill_type=self.cleaned_data['skill_type'])
            except Skill.DoesNotExist:
                # the skill got deleted
                return
            else:
                # create or update the userskill with the new skill
                obj, created = UserSkill.objects.update_or_create(
                                    skill=skill, user=self.user)
            return


SkillFormSet = forms.modelformset_factory(
    Skill,
    form=SkillForm,
    extra=0,
)
