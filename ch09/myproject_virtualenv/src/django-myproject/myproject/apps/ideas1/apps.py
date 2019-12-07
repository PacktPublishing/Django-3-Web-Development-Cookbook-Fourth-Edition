from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Ideas1AppConfig(AppConfig):
    name = "myproject.apps.ideas1"
    verbose_name = _("Ideas with Categories using MPTT")
