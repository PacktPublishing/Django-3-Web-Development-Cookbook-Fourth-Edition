from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ViralVideosAppConfig(AppConfig):
    name = "viral_videos"
    verbose_name = _("Viral Videos")

    def ready(self):
        from .signals import inform_administrators
        from .checks import settings_check
