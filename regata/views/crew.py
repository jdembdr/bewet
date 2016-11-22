from __future__ import absolute_import
from gettext import gettext as _

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView, DetailView

from registration.backends.hmac.views import RegistrationView
from registration import signals

from regata.models.crew import Crew
from regata.forms.crew import CrewProfileForm, UserForm

class WelcomeView(TemplateView):
    template_name = "regata/welcome.html"

class CrewUpdateView(TemplateView):
    template_name = "regata/crew_update.html"
    model = Crew
    form_class = CrewProfileForm
    success_url = '#'

    def get_object(self):
        return Crew.objects.get(user=self.request.user)

def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = CrewProfileForm(request.POST, request.FILES, instance=request.user.crew)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('regata:profile')
        else:
            messages.error(request, _('Please correct errors below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = CrewProfileForm(instance=request.user.crew)
    return render(request, 'regata/crew_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



