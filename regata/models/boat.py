from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

class Boat(models.Model):
    picture = models.ImageField(upload_to='boats/%Y/%m/%d', default='default-boat.png', blank=True, null=True)
    name = models.CharField(max_length=30)
    length = models.IntegerField()
    sail_number = models.IntegerField()
    boat_type = models.CharField(max_length=30)
    build_year = models.IntegerField()
    owner = models.CharField(max_length=30)
    description = models.TextField(max_length= 500)

    # Foreign keys
    skipper = models.ForeignKey('Crew')
    club = models.ForeignKey('Club')
    zone = models.ForeignKey('Zone')

