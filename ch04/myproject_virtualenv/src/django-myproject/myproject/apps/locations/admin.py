from django.contrib.gis import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.OSMGeoAdmin):
    pass