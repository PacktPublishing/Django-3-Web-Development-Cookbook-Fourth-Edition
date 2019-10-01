import contextlib
import os
import uuid
from collections import namedtuple

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django.contrib.gis.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now as timezone_now

from myproject.apps.core.models import CreationModificationDateBase, UrlBase

RATING_CHOICES = ((1, "★☆☆☆☆"), (2, "★★☆☆☆"), (3, "★★★☆☆"), (4, "★★★★☆"), (5, "★★★★★"))

COUNTRY_CHOICES = getattr(settings, "COUNTRY_CHOICES", [])

Geoposition = namedtuple("Geoposition", ["longitude", "latitude"])


def upload_to(instance, filename):
    now = timezone_now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"locations/{now:%Y/%m}/{instance.pk}{extension}"


class Location(CreationModificationDateBase, UrlBase):
    uuid = models.UUIDField(primary_key=True, default=None, editable=False)
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"))
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(
        _("Street address (2nd line)"), max_length=255, blank=True
    )
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    country = models.CharField(
        _("Country"), choices=COUNTRY_CHOICES, max_length=255, blank=True
    )
    geoposition = models.PointField(blank=True, null=True)
    picture = models.ImageField(
        _("Picture"), upload_to=upload_to
    )
    picture_desktop = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(1024, 512)],
        format="JPEG",
        options={"quality": 100},
    )
    picture_tablet = ImageSpecField(
        source="picture", processors=[ResizeToFill(800, 400)], format="PNG"
    )
    picture_mobile = ImageSpecField(
        source="picture", processors=[ResizeToFill(728, 250)], format="PNG"
    )
    rating = models.PositiveIntegerField(
        _("Rating"), choices=RATING_CHOICES, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.name

    def get_url_path(self):
        return reverse("locations:location_detail", kwargs={"pk": self.pk})

    def set_pk(self):
        self.pk = uuid.uuid4()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_pk()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage
        if self.picture:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(self.picture_desktop.path)
                default_storage.delete(self.picture_tablet.path)
                default_storage.delete(self.picture_mobile.path)
            self.picture.delete()
        super().delete(*args, **kwargs)

    def get_geoposition(self):
        if not self.geoposition:
            return None
        return Geoposition(self.geoposition.coords[0], self.geoposition.coords[1])

    def set_geoposition(self, longitude, latitude):
        self.geoposition = f"SRID=4326;POINT ({longitude} {latitude})"
