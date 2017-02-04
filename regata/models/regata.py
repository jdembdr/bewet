from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

class Grade(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)

class Jauge(models.Model):
    name = models.CharField(max_length=03)
    description = models.TextField(max_length=300)

class Tour(models.Model):
    name = models.CharField(max_length=100)
    site = models.URLField(max_length=100)

class Regata(models.Model):
    regata_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    club = models.ForeignKey('Club')
    start = models.DateField()
    end = models.DateField()
    jauge = models.ForeignKey('Jauge', null=True)
    grade = models.ForeignKey('Grade', null=True)

