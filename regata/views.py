from django.shortcuts import render
from django.contrib.auth.models import User

from registration.backends.hmac.views import RegistrationView
from registration import signals

# Create your views here.

def home(request):
    return render(request, template_name='regata/home.html', context=None)

class BewetRegistrationView(RegistrationView):
    """
    Ensure unicity of emails adresses when user register to avoid multiple  due to accounts with social_authentication
    """

    template_name="regata/registration_form.html"

    def register(self, form):
        try:
            # check if email is already registrered
            user = User.objects.get(email=form.cleaned_data['email'])
        except User.DoesNotExist:
            return super(self, RegistrationView).register(form)

        # If user has social_auth, update user password
        user.set_password(form.cleaned_data.get('password1'))
        user.username = form.cleaned_data.get('username')
        user.is_active = False
        user.save()

        self.send_activation_email(user)

        signals.user_registered.send(sender=self.__class__,
                                 user=user,
                                 request=self.request)
        return user

def video(request):
    return render(request, template_name='regata/video.html', context=None)

