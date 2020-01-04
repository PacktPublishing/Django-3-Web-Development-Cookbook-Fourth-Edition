# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


app_name = 'likes'
urlpatterns = [
    url(
        regex="^Like/~create/$",
        view=views.LikeCreateView.as_view(),
        name='Like_create',
    ),
    url(
        regex="^Like/(?P<pk>\d+)/~delete/$",
        view=views.LikeDeleteView.as_view(),
        name='Like_delete',
    ),
    url(
        regex="^Like/(?P<pk>\d+)/$",
        view=views.LikeDetailView.as_view(),
        name='Like_detail',
    ),
    url(
        regex="^Like/(?P<pk>\d+)/~update/$",
        view=views.LikeUpdateView.as_view(),
        name='Like_update',
    ),
    url(
        regex="^Like/$",
        view=views.LikeListView.as_view(),
        name='Like_list',
    ),
	]
