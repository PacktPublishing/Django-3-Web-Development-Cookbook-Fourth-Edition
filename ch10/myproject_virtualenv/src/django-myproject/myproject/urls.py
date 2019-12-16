from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemaps_views
from django.contrib.sitemaps import GenericSitemap

from myproject.apps.music.views import RESTSongList, RESTSongDetail

from myproject.apps.music.models import Song

## Tastypie doesn't yet work with Django 3.0
# from tastypie.api import Api
# from myproject.apps.music.api import SongResource

# v1_api = Api(api_name="v1")
# v1_api.register(SongResource())


class MySitemap(GenericSitemap):
    limit = 50

    def location(self, obj):
        return obj.get_url_path()


song_info_dict = {
    "queryset": Song.objects.all(),
    "date_field": "modified",
}
sitemaps = {"music": MySitemap(song_info_dict, priority=1.0)}


urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("rest-api/songs/", RESTSongList.as_view(), name="rest_song_list"),
    path(
        "rest-api/songs/<uuid:pk>/", RESTSongDetail.as_view(), name="rest_song_detail"
    ),
    # Sitemap
    path("sitemap.xml", sitemaps_views.index, {"sitemaps": sitemaps}),
    path(
        "sitemap-<str:section>.xml",
        sitemaps_views.sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

urlpatterns += i18n_patterns(
    # path("tastypie-api/", include(v1_api.urls)),
    path("admin/", admin.site.urls),
    path("songs/", include("myproject.apps.music.urls", namespace="music")),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
