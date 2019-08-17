from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Example:
SETTING_1 = getattr(settings, "MAGAZINE_SETTING_1", "default value")

MEANING_OF_LIFE = getattr(settings, "MAGAZINE_MEANING_OF_LIFE", 42)

ARTICLE_THEME_CHOICES = getattr(
    settings,
    "MAGAZINE_ARTICLE_THEME_CHOICES",
    [
        ('futurism', _("Futurism")),
        ('nostalgia', _("Nostalgia")),
        ('sustainability', _("Sustainability")),
        ('wonder', _("Wonder")),
    ]
)
