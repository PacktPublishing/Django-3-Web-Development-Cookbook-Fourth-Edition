from django.views.generic import ListView, DetailView

from .models import Article


class ArticleList(ListView):
    model = Article
    paginate_by = 10


class ArticleDetail(DetailView):
    model = Article
    context_object_name = "article"
