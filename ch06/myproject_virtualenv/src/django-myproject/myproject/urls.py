from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = i18n_patterns(
    path("", include("social_django.urls", namespace="social")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
