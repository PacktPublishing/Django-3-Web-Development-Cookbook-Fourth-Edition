from django.urls import path

from .views import ProductDetail


urlpatterns = [
    path('<slug:slug>/', ProductDetail.as_view(),
         name="product-detail"),
]
