from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LikesAppConfig(AppConfig):
    name = "myproject.apps.likes"
    verbose_name = _("Likes")
