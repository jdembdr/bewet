from __future__ import absolute_import

from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, DetailView

from regata.models.regata import Regata
from regata.models.clubs import Club

class CalendarView(ListView):
    model = Regata

class RegataView(DetailView):
    model = Regata

class ClubView(DetailView):
    model = Club
