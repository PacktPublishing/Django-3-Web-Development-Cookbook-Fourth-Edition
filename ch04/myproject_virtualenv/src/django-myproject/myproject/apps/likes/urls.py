from django.urls import path

from .views import json_set_like


urlpatterns = [
    path("<int:content_type_id>/<int:object_id>/",
         json_set_like,
         name="json-set-like")
]
