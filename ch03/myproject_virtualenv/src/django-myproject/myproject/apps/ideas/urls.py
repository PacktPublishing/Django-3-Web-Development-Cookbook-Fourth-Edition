from django.urls import path

from .views import (
    IdeaList,
    IdeaDetail,
    add_idea,
    change_idea,
    delete_idea,
    idea_list,
    IdeaListView,
    idea_handout_pdf,
    search_with_elasticsearch,
)

urlpatterns = [
    # path('', IdeaList.as_view(), name='idea_list'),
    # path('', idea_list, name='idea_list'),
    path("", IdeaListView.as_view(), name="idea_list"),
    path("search/", search_with_elasticsearch, name="search_ideas"),
    path("add/", add_idea, name="add_idea"),
    path("<uuid:pk>/", IdeaDetail.as_view(), name="idea_detail"),
    path(
        "<uuid:pk>/handout/",
        idea_handout_pdf,
        name="idea_handout",
    ),
    path(
        "<uuid:pk>/handout-preview/",
        IdeaDetail.as_view(template_name="ideas/idea_handout_pdf.html"),
        name="idea_handout_preview",
    ),
    path("<uuid:pk>/change/", change_idea, name="change_idea"),
    path("<uuid:pk>/delete/", delete_idea, name="delete_idea"),
]
