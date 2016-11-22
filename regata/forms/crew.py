from __future__ import absolute_import
from datetime import date
from django.forms import widgets
from django import forms
from regata.models.crew import Crew
from django.contrib.auth.models import User


class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        # create choices for days, months, years
        # example below, the rest snipped for brevity.
        years = [(year, year) for year in (2011, 2012, 2013)]
        months = [(month, month) for month in range(1,12)]
        days= [(day, day) for day in range(1,31)]

        _widgets = (
            widgets.Select(attrs=attrs, choices=days),
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            D = date(
                day=int(datelist[0]),
                month=int(datelist[1]),
                year=int(datelist[2]),
            )
        except ValueError:
            return ''
        else:
            return str(D)

class CrewProfileForm(forms.ModelForm):
    picture = forms.FileInput()
    birth_date = forms.DateInput( widget=DateSelectorWidget )

    class Meta:
        model = Crew
        fields = ['picture', 'birth_date',
                'gender', 'size', 'weight',]
        """
                'licence_id','isaf_id','level',
                'language', 'description', 'best_results']
        """

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

