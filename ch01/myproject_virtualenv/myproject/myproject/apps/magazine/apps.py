from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MagazineAppConfig(AppConfig):
    name = "myproject.apps.magazine"
    verbose_name = _("Magazine")

    def ready(self):
        from . import signals
