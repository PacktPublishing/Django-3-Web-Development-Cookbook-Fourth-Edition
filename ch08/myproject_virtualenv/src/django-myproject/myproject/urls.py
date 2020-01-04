from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from myproject.apps.categories1 import views as categories1_views

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "idea-categories1/",
        categories1_views.IdeaCategoryList.as_view(),
        name="idea_categories1",
    ),
    path("ideas1/", include(("myproject.apps.ideas1.urls", "ideas1"), namespace="ideas1")),

)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
