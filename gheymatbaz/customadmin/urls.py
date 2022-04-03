from django.urls import path, re_path
from customadmin.views import all_product, edit_product, add_product, CategoryCreateView, \
    CategoryUpdateView, CategoryDeleteView, BrandCreateView, BrandUpdateView, BrandDeleteView

urlpatterns = [
    path('product/all', all_product),
    path('product/add', add_product, name='add-product'),
    re_path('product/edit/(?P<slug>[-\w]+)/', edit_product),
    # path('categories/all', all_category),
    # path('category/edit/<int:pk>/', edit_category, name='edit-category'),

    path('category/add/', CategoryCreateView.as_view(), name='category-add'),
    path('category/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('brand/add/', BrandCreateView.as_view(), name='brand-add'),
    path('brand/<int:pk>/', BrandUpdateView.as_view(), name='brand-update'),
    path('brand/<int:pk>/delete/', BrandDeleteView.as_view(), name='brand-delete'),

]
