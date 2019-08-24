from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from myproject.apps.core.admin import get_multilingual_field_names

from .models import Idea


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Author and Category"), {
            "fields": ["author", "categories"],
        }),
        (_("Title and Content"), {
            "fields": get_multilingual_field_names("title") +
                      get_multilingual_field_names("content")
        }),
        (_("SEO"), {
            "fields": ["meta_keywords", "meta_description", "meta_author", "meta_copyright"]
        }),
    ]
    filter_horizontal = ["categories"]