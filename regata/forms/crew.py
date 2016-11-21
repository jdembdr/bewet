from django import forms
from regata.models.crew import Crew


class CrewProfileForm(forms.ModelForm):
    class Meta:
        model = Crew
        exclude = ['id', 'email', 'password']
