from __future__ import absolute_import

from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, DetailView

from regata.models.regata import Regata

class RegataView(DetailView):
    model = Regata
