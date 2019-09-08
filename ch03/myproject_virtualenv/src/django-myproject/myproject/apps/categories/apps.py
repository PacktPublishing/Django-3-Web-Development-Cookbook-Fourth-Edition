from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoriesAppConfig(AppConfig):
    name = "myproject.apps.categories"
    verbose_name = _("Categories")
