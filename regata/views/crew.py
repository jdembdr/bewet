from __future__ import absolute_import
from gettext import gettext as _

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView, CreateView

from registration.backends.hmac.views import RegistrationView
from registration import signals

from regata.models.crew import Crew
from regata.forms.crew import CrewProfileForm, UserForm

from regata.models.boat import Boat
from regata.forms.boat import BoatProfileForm

class WelcomeView(TemplateView):
    template_name = "regata/welcome.html"


def boat_profile(request):
    boats = Boat.objects.filter(skipper = request.user.crew)
    if len(boats) > 0 :
        return BoatUpdateView.as_view()(request, pk=boats[0].pk)
    else :
        return BoatCreateView.as_view()(request)

class BoatCreateView(CreateView):
    model = Boat
    form_class = BoatProfileForm
    template_name = 'regata/snippet/boat_profile.html'
    success_url = 'regata:settings'

    def form_valid(self, form):
        form.instance.skipper = self.request.user.crew
        return super(BoatCreateView, self).form_valid(form)


class BoatUpdateView(UpdateView):
    model = Boat
    form_class = BoatProfileForm
    template_name = 'regata/snippet/boat_profile.html'
    success_url = 'regata:settings'

    def get_context_data(self, **kwargs):
        context = super(BoatUpdateView, self).get_context_data(**kwargs)
        context['boat_list'] = self.model.objects.filter( skipper= self.request.user.crew)
        return context

def user_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = CrewProfileForm(request.POST, request.FILES, instance=request.user.crew)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('regata:settings')
        else:
            messages.error(request, _('Please correct errors below.'))
            return
    else:
        user_form = UserForm(instance=request.user)
        profile_form = CrewProfileForm(instance=request.user.crew)
    return render(request, 'regata/snippet/user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def user_settings(request):
    return render(request, 'regata/settings.html', {'form': 'user'})



