from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from myproject.apps.auth0_login import views as auth0_views

urlpatterns = i18n_patterns(
    path("", auth0_views.index, name="index"),
    path("dashboard/", auth0_views.dashboard, name="dashboard"),
    path("logout/", auth0_views.logout, name="auth0_logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("social_django.urls")),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("management/", admin.site.urls),
    path("ideas/", include(("myproject.apps.ideas.urls", "ideas"), namespace="ideas")),
    path("videos/", include("myproject.apps.viral_videos.urls")),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
