import json
from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings


def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, "index.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def logout(request):
    log_out(request)
    return_to = urlencode({"returnTo": request.build_absolute_uri("/")})
    logout_url = "https://%s/v2/logout?client_id=%s&%s" % (
        settings.SOCIAL_AUTH_AUTH0_DOMAIN,
        settings.SOCIAL_AUTH_AUTH0_KEY,
        return_to,
    )
    return redirect(logout_url)
