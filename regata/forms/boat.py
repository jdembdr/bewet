from __future__ import absolute_import
from gettext import gettext as _

from django import forms
from regata.models.boat import Boat

class BoatProfileForm(forms.ModelForm):
    picture = forms.FileField( widget=forms.FileInput)

    class Meta:
        model = Boat
        fields = ['picture', 'name', 'length', 'sail_number',
                'boat_type', 'build_year', 'owner',
                'description', 'club', 'zone']

