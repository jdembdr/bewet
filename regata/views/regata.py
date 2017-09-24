from __future__ import absolute_import

from django.shortcuts import render
from django.views.generic import View, TemplateView, UpdateView, DetailView, ListView
from django.http import JsonResponse
from django.core import serializers

from regata.models.regata import Regata
from regata.models.club import Club

class CalendarView(ListView):
    model = Regata

class RegataView(DetailView):
    model = Regata

class ClubView(DetailView):
    model = Club

class MapRequestView(View):
    def post(self, request, *args, **kw):
        queryset = Club.objects.all()
        return JsonResponse(serializers.serialize('geojson', queryset, geometry_field='position', fields=('name',)), safe=False)

    get = post
