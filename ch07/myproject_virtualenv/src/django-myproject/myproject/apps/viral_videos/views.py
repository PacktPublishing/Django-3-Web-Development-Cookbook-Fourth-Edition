import datetime, logging

from django.conf import settings
from django.db import models
from django.shortcuts import render, get_object_or_404

from .models import ViralVideo

POPULAR_FROM = getattr(
    settings, "VIRAL_VIDEOS_POPULAR_FROM", 500
)

logger = logging.getLogger(__name__)


def viral_video_detail(request, pk):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    qs = ViralVideo.objects.annotate(
        total_views=models.F("authenticated_views") +
                          models.F("anonymous_views"),
        label=models.Case(
            models.When(total_views__gt=POPULAR_FROM,
                        then=models.Value("popular")),
            models.When(created__gt=yesterday,
                        then=models.Value("new")),
            default=models.Value("cool"),
            output_field=models.CharField()))

    # DEBUG: check the SQL query that Django ORM generates
    logger.debug(f"Query: {qs.query}")

    qs = qs.filter(pk=pk)
    if request.user.is_authenticated:
        qs.update(authenticated_views=models.F(
            "authenticated_views") + 1)
    else:
        qs.update(anonymous_views=models.F(
            "anonymous_views") + 1)

    video = get_object_or_404(qs)

    return render(request,
                  "viral_videos/viral_video_detail.html",
                  {'video': video})
