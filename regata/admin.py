from django.contrib import admin
from regata.models.crew import Crew
from regata.models.boat import Boat
from regata.models.regata import Regata
from regata.models.zone import Zone
from regata.models.club import Club

# Register your models here.
admin.site.register(Crew)
admin.site.register(Boat)
admin.site.register(Zone)
admin.site.register(Regata)
admin.site.register(Club)

