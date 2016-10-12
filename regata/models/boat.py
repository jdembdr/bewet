from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

class Boat(models.Model):
    picture = models.ImageField()
    name = models.CharField(max_length=30)
    length = models.IntegerField()
    sail_number = models.IntegerField()
    club = models.ForeignKey('Club')
    zone = models.ForeignKey('Zone')
    boat_type = models.CharField(max_length=30)
    build_year = models.IntegerField()
    owner = models.CharField(max_length=30)
    skipper = models.ForeignKey('Crew')

