from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from pothole.models import Pothole, PotholeRepair

# Register your models here.
admin.site.register(Pothole, LeafletGeoAdmin)
admin.site.register(PotholeRepair)