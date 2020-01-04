from django.contrib import admin

from .models import ViralVideo


@admin.register(ViralVideo)
class ViralVideoAdmin(admin.ModelAdmin):
    list_display = ["title", "created", "modified", "creator"]
