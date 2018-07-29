from django import forms

from . import models


class ProjectForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
                    attrs={'class': 'circle--input--h1',
                           'placeholder': 'Project Title'}))
    description = forms.CharField(widget=forms.Textarea(
                        attrs={'placeholder': 'project description...'}))
    timeline = forms.CharField(widget=forms.TextInput(
                    attrs={'class': 'circle--textarea--input',
                           'placeholder': 'timeline'}))
    requirements = forms.CharField(widget=forms.TextInput(
                    attrs={'class': 'circle--textarea--input',
                           'placeholder': 'requirements'}))

    class Meta:
        model = models.Project
        fields = (
            'name',
            'description',
            'timeline',
            'requirements'
        )


class PositionForm(forms.ModelForm):
    # skill = forms.CharField(widget=forms.TextInput(
    #                 attrs={'class': 'circle--textarea--input',
    #                        'placeholder': 'title'}))
    skill = forms.ModelChoiceField(
                            queryset=models.Skill.objects.all(),
                            )
    description = forms.CharField(widget=forms.Textarea(
                        attrs={'placeholder': 'position description...'}))    

    class Meta:
        model = models.Position
        fields = (
                'skill',
                'description',
            )

    # def clean_skill(self):
    #     '''
    #         before we validate the skill we nee to check if a new skill
    #         type has been added and create a new record
    #     '''
    #     data = self.cleaned_data['skill']
    #     if not models.Skill.objects.filter(skill_type=data):
    #                 skill = models.Skill.objects.create(
    #                                             skill_type=data
    #                                                  )
    #     else:
    #         skill = models.Skill.objects.get(skill_type=data)
    #     return skill


class BasePositionFormSet(forms.BaseModelFormSet):
    '''
    by deafult a formset gets all objects in the model - creating a base class
    with no objects will allow for an empty position form to be sent into
    the context

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.queryset is None:  # this is ood !!!
            self.queryset = models.Position.objects.none()


PositionFormSet = forms.modelformset_factory(
    models.Position,
    form=PositionForm,
    extra=1,
    formset=BasePositionFormSet
)
