from django.urls import path, re_path
from shop.views import single_product, list_all, index, category_list

urlpatterns = [
    path('index/', index, name='index'),

    re_path(r'category/(?P<slug>[-\w]+)/', category_list, name='category-archive'),
    re_path(r'product/(?P<slug>[-\w]+)/', single_product, name='single-product'),
    path('product/', list_all, name='archive-product'),

]
