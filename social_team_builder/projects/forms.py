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

    # def save(self):
    #     '''[summary]
    #     '''
    #     pdb.set_trace()
    #     if self.changed_data:
    #         if self.cleaned_data['skill'] != '':
    #             # position = get_object_or_404(models.Position,
    #             #                              id=self.cleaned_data['id'].id)
    #             # position.skill = self.cleaned_data['skill']
    #             # position.save() 
    #             self.save()
    #         return


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


PositionFormSet = forms.modelformset_factory(
    models.Position,
    form=PositionForm,
    extra=1,
    formset=BasePositionFormSet
)
