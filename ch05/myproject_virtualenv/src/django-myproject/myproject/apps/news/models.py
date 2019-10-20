from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from myproject.apps.core.models import CreationModificationDateBase, UrlBase


class ArticleManager(models.Manager):
    def random_published(self):
        return self.filter(
            publishing_status=self.model.PUBLISHING_STATUS_PUBLISHED,
        ).order_by("?")


class Article(CreationModificationDateBase, UrlBase):
    PUBLISHING_STATUS_DRAFT, PUBLISHING_STATUS_PUBLISHED = "d", "p"
    PUBLISHING_STATUS_CHOICES = (
        (PUBLISHING_STATUS_DRAFT, _("Draft")),
        (PUBLISHING_STATUS_PUBLISHED, _("Published")),
    )
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200)
    content = models.TextField(_("Content"))
    publishing_status = models.CharField(
        _("Publishing status"),
        max_length=1,
        choices=PUBLISHING_STATUS_CHOICES,
        default=PUBLISHING_STATUS_DRAFT,
    )

    custom_manager = ArticleManager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title

    def get_url_path(self):
        return reverse("news:article_detail", kwargs={"slug": self.slug})
