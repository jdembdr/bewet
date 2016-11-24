from __future__ import absolute_import
from gettext import gettext as _
from datetime import date
from django.forms import widgets
from django import forms
from regata.models.crew import Crew
from django.contrib.auth.models import User
from django.forms import extras

class BoatProfileForm(forms.ModelForm):
    picture = forms.FileField( widget=forms.FileInput)

    class Meta:
        model = Crew
        fields = ['picture', 'name', 'length', 'sail_number',
                'boat_type', 'build_year', 'owner',
                'description', 'club', 'zone']

