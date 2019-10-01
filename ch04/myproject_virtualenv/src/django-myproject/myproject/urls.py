from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from myproject.apps.core import views as core_views


urlpatterns = i18n_patterns(
    path("", lambda request: redirect("locations:location_list")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("locations/", include(("myproject.apps.locations.urls", "locations"), namespace="locations")),
    path("js-settings/", core_views.js_settings, name="js_settings"),
)

urlpatterns += [
    path(
        "upload-file/",
        core_views.upload_file,
        name="upload_file",
    ),
    path(
        "delete-file/",
        core_views.delete_file,
        name="delete_file",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
