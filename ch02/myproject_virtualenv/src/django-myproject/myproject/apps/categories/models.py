from django.db import models
from django.utils.translation import gettext_lazy as _

from myproject.apps.core.model_fields import MultilingualCharField


class Category(models.Model):
    title = MultilingualCharField(
        _("Title"),
        max_length=200,
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title

    def get_ideas_without_this_category(self):
        from myproject.apps.ideas.models import Idea
        return Idea.objects.exclude(categories=self)
