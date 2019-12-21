from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

import debug_toolbar


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("viral-videos/", include("myproject.apps.viral_videos.urls", namespace="viral_videos")),
)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
