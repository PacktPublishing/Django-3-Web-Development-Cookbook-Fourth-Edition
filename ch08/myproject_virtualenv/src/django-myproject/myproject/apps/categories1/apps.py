from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Categories1AppConfig(AppConfig):
    name = "myproject.apps.categories1"
    verbose_name = _("Categories using MPTT")
