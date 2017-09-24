from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib.gis.db import models

class Club(models.Model):
    club_id = models.TextField('FFV club identifiant', primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField(default='')
    city = models.TextField(default='')
    postal = models.TextField(default='')
    phone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField(default='')
    site = models.URLField(default='')
    summary = models.TextField(default='')
    description = models.TextField(default='')
    scheduling = models.TextField(default='')
    position = models.PointField(blank=True, null=True)



