from django.urls import path

from .views import (
    IdeaDetail,
    add_or_change_idea,
    delete_idea,
    IdeaListView,
)

urlpatterns = [
    path("", IdeaListView.as_view(), name="idea_list"),
    path("add/", add_or_change_idea, name="add_idea"),
    path("<uuid:pk>/", IdeaDetail.as_view(), name="idea_detail"),
    path("<uuid:pk>/change/", add_or_change_idea, name="change_idea"),
    path("<uuid:pk>/delete/", delete_idea, name="delete_idea"),
]
