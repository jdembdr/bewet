from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

class Zone(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name
