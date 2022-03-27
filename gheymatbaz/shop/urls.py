from django.urls import path, re_path
from shop.views import single_product, list_all


urlpatterns = [
    re_path(r'detail/(?P<slug>[-\w]+)/', single_product, name='single-product'),
    path('product/', list_all, name='archive-product'),
]
