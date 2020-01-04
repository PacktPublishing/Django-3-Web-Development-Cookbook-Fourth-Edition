from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Ideas2AppConfig(AppConfig):
    name = "myproject.apps.ideas2"
    verbose_name = _("Ideas with Categories using TreeBeard")
