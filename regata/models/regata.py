from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

class Grade(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.TextField(max_length=300)

class Class(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
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
    classes = models.ManyToManyField('Class')
    grades = models.ManyToManyField('Grade')

