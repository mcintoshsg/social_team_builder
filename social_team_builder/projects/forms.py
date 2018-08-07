from django.shortcuts import get_object_or_404
from django import forms

from . import models

import pdb

class SkillForm(forms.ModelForm):
    skill = forms.CharField(widget=forms.TextInput(
                    attrs={'class': 'circle--textarea--input',
                           'placeholder': 'title'}))


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
    skill = forms.ModelChoiceField(queryset=models.Skill.objects.all())
    description = forms.CharField(widget=forms.Textarea(
                        attrs={'placeholder': 'position description...'}))

    class Meta:
        model = models.Position
        fields = (
                'skill',
                'description',
            )
  

    # def save(self):
    #     position = super(PositionForm, self).save(commit=False)
    #     pdb.set_trace()
    #     project = models.Project.objects.last()
    #     if self.cleaned_data['skill']:
    #         obj = models.Position.objects.filter(
    #                                         project=project,
    #                                         skill=self.cleaned_data['skill']
    #                                         )
    #         if obj:
    #             raise forms.ValidationError('wldkjwghdwh')
    #         else:
    #             position.project = project
    #             super(PositionForm, self).save(self)
    #     return

class BasePositionFormSet(forms.BaseModelFormSet):
    '''
    by deafult a formset gets all objects in the model - creating a base class
    with no objects will allow for an empty position form to be sent into
    the context

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.queryset is None:  # this is odd !!!
            self.queryset = models.Position.objects.none()

    def clean(self):
        if any(self.errors):
            return
        values = set()
        for form in self.forms:
            if form.cleaned_data:
                value = form.cleaned_data['skill']
                if value in values:
                    raise forms.ValidationError(
                            'Duplicate values for position are not allowed')
                values.add(value)


PositionFormSet = forms.modelformset_factory(
    models.Position,
    form=PositionForm,
    extra=1,
    formset=BasePositionFormSet
)
