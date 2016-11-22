from __future__ import absolute_import
"""bewet URL Configuration

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
import datetime

from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib import admin
from django.conf import settings

import landing.views
import regata.views

def test(request):
    return render(request, "test.html", {'time' : datetime.datetime.now()})


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^soon/', landing.views.comingsoon),
    url(r'^test/', test),
    url(r'^$', regata.views.home, name="homepage"),
    # Other URL patterns ...

    url(r'^accounts/register/', regata.views.BewetRegistrationView.as_view(),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url('', include('regata.urls', namespace='regata')),
    url('', include('sandbox.urls', namespace='sandbox')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [ url(r'^__debug__/', include(debug_toolbar.urls)), ]
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
