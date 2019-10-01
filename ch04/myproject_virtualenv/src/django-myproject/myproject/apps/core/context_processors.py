from django.conf import settings

def website_url(request):
    return {
        "WEBSITE_URL": settings.WEBSITE_URL,
    }