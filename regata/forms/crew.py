from __future__ import absolute_import
from django import forms
from regata.models.crew import Crew
from django.contrib.auth.models import User

class CrewProfileForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ['picture', 'birth_date']
        """
                'gender', 'size', 'weight',
                'licence_id','isaf_id','level',
                'language', 'description', 'best_results']
        """

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

