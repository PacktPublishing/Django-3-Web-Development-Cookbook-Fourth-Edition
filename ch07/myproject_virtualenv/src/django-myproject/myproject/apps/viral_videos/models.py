import re
from django.db import models
from django.utils.translation import ugettext_lazy as _

from myproject.apps.core.models import CreationModificationDateBase, UrlBase


class ViralVideo(CreationModificationDateBase, UrlBase):
    title = models.CharField(
        _("Title"),
        max_length=200,
        blank=True)
    embed_code = models.TextField(
        _("YouTube embed code"),
        blank=True)
    anonymous_views = models.PositiveIntegerField(
        _("Anonymous impressions"),
        default=0)
    authenticated_views = models.PositiveIntegerField(
        _("Authenticated impressions"),
        default=0)

    class Meta:
        verbose_name = _("Viral video")
        verbose_name_plural = _("Viral videos")

    def __str__(self):
        return self.title

    def get_url_path(self):
        from django.urls import reverse
        return reverse("viral-video-detail",
                       kwargs={"pk": str(self.pk)})

    def get_thumbnail_url(self):
        if not hasattr(self, "_thumbnail_url_cached"):
            self._thumbnail_url_cached = ""
            url_pattern = re.compile(
                r'src="https://www.youtube.com/embed/([^"]+)"'
            )
            match = url_pattern.search(self.embed_code)
            if match:
                video_id = match.groups()[0]
                self._thumbnail_url_cached = (
                    f"https://img.youtube.com/vi/{video_id}/0.jpg"
                )
        return self._thumbnail_url_cached