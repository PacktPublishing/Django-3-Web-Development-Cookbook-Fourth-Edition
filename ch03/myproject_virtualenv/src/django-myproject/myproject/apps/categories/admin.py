from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from myproject.apps.core.admin import LanguageChoicesForm

from .models import Category, CategoryTranslations


class CategoryTranslationsForm(LanguageChoicesForm):
    class Meta:
        model = CategoryTranslations
        fields = "__all__"


class CategoryTranslationsInline(admin.StackedInline):
    form = CategoryTranslationsForm
    model = CategoryTranslations
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTranslationsInline]

    fieldsets = [
        (_("Title"), {
            "fields": ["title"]
        }),
    ]
