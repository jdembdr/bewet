from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Crew)
admin.site.register(models.Boat)
admin.site.register(models.Zone)
admin.site.register(models.Regata)
admin.site.register(models.Club)

