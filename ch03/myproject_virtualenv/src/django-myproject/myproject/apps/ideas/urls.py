from django.urls import path

from .views import IdeaList, IdeaDetail, add_idea, change_idea, delete_idea, idea_list, IdeaListView

urlpatterns = [
    #path('', IdeaList.as_view(), name='idea_list'),
    #path('', idea_list, name='idea_list'),
    path('', IdeaListView.as_view(), name='idea_list'),
    path('add/', add_idea, name='add_idea'),
    path('<uuid:pk>/', IdeaDetail.as_view(), name='idea_detail'),
    path('<uuid:pk>/change/', change_idea, name='change_idea'),
    path('<uuid:pk>/delete/', delete_idea, name='delete_idea'),
]
