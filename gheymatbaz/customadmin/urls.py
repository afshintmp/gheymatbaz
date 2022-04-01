from django.urls import path, re_path
from customadmin.views import all_product, edit_product, add_product, all_category, edit_category

urlpatterns = [
    path('product/all', all_product),
    path('product/add', add_product, name='add-product'),
    re_path('product/edit/(?P<slug>[-\w]+)/', edit_product),
    path('categories/all', all_category),
    path('category/edit/<int:pk>/', edit_category, name='edit-category'),
]
