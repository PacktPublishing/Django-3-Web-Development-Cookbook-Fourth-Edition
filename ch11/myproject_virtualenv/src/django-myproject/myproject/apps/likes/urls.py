from django.urls import path
from .views import json_set_like

app_name = "likes"


urlpatterns = [
    path("<int:content_type_id>/<str:object_id>/", json_set_like, name="json_set_like")
]
