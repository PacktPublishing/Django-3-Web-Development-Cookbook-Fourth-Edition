from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


urlpatterns = i18n_patterns(
    path("", lambda request: redirect("ideas:idea_list")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ideas/", include(("myproject.apps.ideas.urls", "ideas"), namespace="ideas")),
    path("search/", include("haystack.urls")),
)
urlpatterns += [
    path("qr_code/", include("qr_code.urls", namespace="qr_code")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
