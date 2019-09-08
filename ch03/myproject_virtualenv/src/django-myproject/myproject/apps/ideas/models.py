import os
import uuid

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now as timezone_now

from myproject.apps.core.model_fields import TranslatedField
from myproject.apps.core.models import CreationModificationDateBase, UrlBase


def upload_to(instance, filename):
    now = timezone_now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"ideas/{now:%Y/%m}/{instance.pk}{extension}"


class Idea(CreationModificationDateBase, UrlBase):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="authored_ideas",
    )
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))
    picture = models.ImageField(
        _("Picture"), upload_to=upload_to, blank=True, null=True
    )
    picture_large = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(800, 400)],
        format="PNG",
        options={"quality": 60},
    )
    picture_thumbnail = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(150, 150)],
        format="PNG",
        options={"quality": 60},
    )
    categories = models.ManyToManyField(
        "categories.Category",
        verbose_name=_("Categories"),
        related_name="category_ideas",
    )

    translated_title = TranslatedField("title")
    translated_content = TranslatedField("content")

    class Meta:
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")

    def __str__(self):
        return self.title

    def get_url_path(self):
        return reverse("ideas:idea_detail", kwargs={"pk": self.pk})


class IdeaTranslations(models.Model):
    idea = models.ForeignKey(
        Idea,
        verbose_name=_("Idea"),
        on_delete=models.CASCADE,
        related_name="translations",
    )
    language = models.CharField(_("Language"), max_length=7)

    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))

    class Meta:
        verbose_name = _("Idea Translations")
        verbose_name_plural = _("Idea Translations")
        ordering = ["language"]
        unique_together = [["idea", "language"]]

    def __str__(self):
        return self.title


"""
>>> from django.conf import settings
>>> from django.db import models
>>> lang_code = input("Enter language code: ")

>>> if lang_code == settings.LANGUAGE_CODE:
...     qs = Idea.objects.annotate(
...         title_translation=models.F("title"),
...         content_translation=models.F("content"),
...     )
... else:
...     qs = Idea.objects.filter(
...         translations__language=lang_code,
...     ).annotate(
...         title_translation=models.F("translations__title"),
...         content_translation=models.F("translations__content"),
...     )

>>> qs = qs.order_by("title_translation")

>>> for idea in qs:
...     print(idea.title_translation)
"""
