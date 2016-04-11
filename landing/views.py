from django.shortcuts import render

# Create your views here.

def comingsoon(request):
    return render(request,template_name='comingsoon.html',context=None)

def welcome(request):
    return render(request,template_name='welcome.html',context=None)
