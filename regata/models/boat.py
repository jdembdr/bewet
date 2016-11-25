from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

class Boat(models.Model):
    picture = models.ImageField(upload_to='boats/%Y/%m/%d', default='default-boat.png', blank=True, null=True)
    name = models.CharField(max_length=30, null=True)
    length = models.FloatField(blank=True, null=True)
    sail_number = models.CharField(max_length=20, blank=True, null=True)
    boat_type = models.CharField(max_length=30, blank=True, null=True)
    build_year = models.IntegerField( blank=True, null=True)
    owner = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(max_length= 500, blank=True, null=True)

    # Foreign keys
    skipper = models.ForeignKey('Crew')
    club = models.ForeignKey('Club', blank=True,null=True)
    zones = models.ManyToManyField('Zone', related_name="boats", blank=True)

