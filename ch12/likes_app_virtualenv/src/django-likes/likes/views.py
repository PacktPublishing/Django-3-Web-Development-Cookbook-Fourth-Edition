# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	Like,
)


class LikeCreateView(CreateView):

    model = Like


class LikeDeleteView(DeleteView):

    model = Like


class LikeDetailView(DetailView):

    model = Like


class LikeUpdateView(UpdateView):

    model = Like


class LikeListView(ListView):

    model = Like

