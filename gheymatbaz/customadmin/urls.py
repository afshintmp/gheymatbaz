from django.urls import path, re_path
from customadmin.views import admin_product, edit_product, add_product, create_product

urlpatterns = [
    path('product/all', admin_product),
    path('product/add', add_product, name='add-product'),
    path('product/create-product', create_product, name='create-product'),
    re_path('product/edit/(?P<slug>[-\w]+)/', edit_product)
]
