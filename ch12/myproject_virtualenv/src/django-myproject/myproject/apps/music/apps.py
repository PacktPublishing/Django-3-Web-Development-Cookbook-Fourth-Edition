from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MusicAppConfig(AppConfig):
    name = "myproject.apps.music"
    verbose_name = _("Music")
