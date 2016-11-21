from django import forms
from regata.models.crew import Crew


class CrewProfileForm(forms.Form):
    class Meta:
        model = Crew
        exclude = ['id', 'email', 'password']
