import os
import uuid
from collections import namedtuple

from django.contrib.gis.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now as timezone_now

from myproject.apps.core.models import CreationModificationDateBase, UrlBase

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
    picture = models.ImageField(_("Picture"), upload_to=upload_to)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.name

    def get_url_path(self):
        return reverse("locations:location_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.pk = uuid.uuid4()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.picture:
            self.picture.delete()
        super().delete(*args, **kwargs)

    def get_geoposition(self):
        if not self.geoposition:
            return None
        return Geoposition(self.geoposition.coords[0], self.geoposition.coords[1])

    def set_geoposition(self, longitude, latitude):
        from django.contrib.gis.geos import Point
        self.geoposition = Point(longitude, latitude, srid=4326)
