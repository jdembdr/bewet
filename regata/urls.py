
"""bewet/Regata  URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

from .views import video
from .views.crew import WelcomeView, user_settings, user_profile, boat_profile, BoatUpdateView, BoatCreateView

from .views.regata import MapRequestView

urlpatterns = [
        url(r'video', video, name='video'),
        url(r'_clubs', MapRequestView.as_view(), name='_clubs'),
        url(r'welcome/$', WelcomeView.as_view(), name='welcome'),
        url(r'settings/$', user_settings, name='settings'),
        url(r'user_profile/$', user_profile, name='user_profile'),
        url(r'boat_profile/$', boat_profile, name='boat_profile'),
        url(r'boat_profile/$', boat_profile, name='planning_profile'),
]

