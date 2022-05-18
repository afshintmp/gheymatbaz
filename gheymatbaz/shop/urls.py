from django.urls import path, re_path
from shop.views import single_product, list_all, index, category_list, single_brand

urlpatterns = [

    re_path(r'category/(?P<slug>[-\w]+)/', category_list, name='category-archive'),
    re_path(r'product/(?P<slug>[-\w]+)/', single_product, name='single-product'),
    re_path(r'brand/(?P<slug>[-\w]+)/', single_brand, name='archive-brand'),
    path('product/', list_all, name='archive-product'),

]
