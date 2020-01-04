# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (
   Like,
)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass



