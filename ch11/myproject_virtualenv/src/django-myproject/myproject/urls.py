from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from myproject.apps.music.views import RESTSongList, RESTSongDetail


urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("rest-api/songs/", RESTSongList.as_view(), name="rest_song_list"),
    path(
        "rest-api/songs/<uuid:pk>/", RESTSongDetail.as_view(), name="rest_song_detail"
    ),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("songs/", include("myproject.apps.music.urls", namespace="music")),
    path("locations/", include("myproject.apps.locations.urls", namespace="locations")),
    path("likes/", include("myproject.apps.likes.urls", namespace="likes")),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
