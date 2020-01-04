from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsAppConfig(AppConfig):
    name = "myproject.apps.locations"
    verbose_name = _("Locations")
