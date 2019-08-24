from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from myproject.apps.core.admin import LanguageChoicesForm

from .models import Idea, IdeaTranslations


class IdeaTranslationsForm(LanguageChoicesForm):
    class Meta:
        model = IdeaTranslations
        fields = "__all__"


class IdeaTranslationsInline(admin.StackedInline):
    form = IdeaTranslationsForm
    model = IdeaTranslations
    extra = 0


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    inlines = [IdeaTranslationsInline]

    fieldsets = [
        (_("Author and Category"), {
            "fields": ["author", "category"]
        }),
        (_("Title and Content"), {
            "fields": ["title", "content"]
        }),
        (_("SEO"), {
            "fields": ["meta_keywords", "meta_description", "meta_author", "meta_copyright"]
        }),
    ]
