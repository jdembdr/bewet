from __future__ import absolute_import
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView, UpdateView, DetailView

from registration.backends.hmac.views import RegistrationView
from registration import signals

from regata.models.crew import Crew
from regata.forms.crew import CrewProfileForm

class WelcomeView(TemplateView):
    template_name = "regata/welcome.html"

class CrewUpdateView(UpdateView):
    template_name = "regata/crew_update.html"
    model = Crew
    form_class = CrewProfileForm
    success_url = '#'

    def get_object(self):
        return Crew.objects.get(user=self.request.user)





