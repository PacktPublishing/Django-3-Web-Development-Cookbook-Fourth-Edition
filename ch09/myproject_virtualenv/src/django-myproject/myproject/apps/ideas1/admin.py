from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Idea


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Author and Category"), {"fields": ["author", "categories"]}),
        (_("Title and Content"), {"fields": ["title", "content", "picture"]}),
        (_("Ratings"), {"fields": ["rating"]}),
    ]
    filter_horizontal = ["categories"]