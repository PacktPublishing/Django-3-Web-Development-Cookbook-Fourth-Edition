from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = "myproject.apps.accounts"
    verbose_name = _("Accounts")

    def ready(self):
        pass


class SocialDjangoConfig(AppConfig):
    name = 'social_django'
    verbose_name = _('Social Authentication')
