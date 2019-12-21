from ._base import *

DEBUG = True

WEBSITE_URL = "http://127.0.0.1:8000"  # without trailing slash
MEDIA_URL = f"{WEBSITE_URL}/media/"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
