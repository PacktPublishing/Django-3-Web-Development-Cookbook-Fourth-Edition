from django.views.generic import ListView

from .models import Category


class IdeaCategoryList(ListView):
    model = Category
    template_name = "categories1/category_list.html"
    context_object_name = "categories"
