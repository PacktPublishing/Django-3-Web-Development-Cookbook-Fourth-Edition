from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass