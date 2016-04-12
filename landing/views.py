from django.shortcuts import render

from .models import ExternalMailingListSubscriber

# Create your views here.

def comingsoon(request):
    if request.POST:
        if not ExternalMailingListSubscriber.objects.filter(email=request.POST['email']):
            email_subscriber = ExternalMailingListSubscriber.objects.create( email=request.POST['email'] )
            email_subscriber.save()

# send email to confirm subscription
    return render(request,template_name='comingsoon.html',context=None)

def welcome(request):
    return render(request,template_name='welcome.html',context=None)
