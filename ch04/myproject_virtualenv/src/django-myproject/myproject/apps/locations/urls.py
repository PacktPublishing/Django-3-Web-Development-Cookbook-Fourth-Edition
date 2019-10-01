from django.urls import path

from .views import (
    LocationList,
    LocationDetail,
    add_or_change_location,
    delete_location,
)

urlpatterns = [
    path("", LocationList.as_view(), name="location_list"),
    path("add/", add_or_change_location, name="add_location"),
    path("<uuid:pk>/", LocationDetail.as_view(), name="location_detail"),
    path("<uuid:pk>/change/", add_or_change_location, name="change_location"),
    path("<uuid:pk>/delete/", delete_location, name="delete_location"),
]
