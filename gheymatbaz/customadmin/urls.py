from django.urls import path, re_path
from customadmin.views import edit_product, CategoryCreateView, \
    CategoryUpdateView, CategoryDeleteView, BrandCreateView, BrandUpdateView, BrandDeleteView, ProductListView, \
    ProductCreateView

urlpatterns = [


    # re_path('product/edit/(?P<slug>[-\w]+)/', edit_product),
    # path('categories/all', all_category),
    # path('category/edit/<int:pk>/', edit_category, name='edit-category'),

    path('category/add/', CategoryCreateView.as_view(), name='category-add'),
    path('category/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('brand/add/', BrandCreateView.as_view(), name='brand-add'),
    path('brand/<int:pk>/', BrandUpdateView.as_view(), name='brand-update'),
    path('brand/<int:pk>/delete/', BrandDeleteView.as_view(), name='brand-delete'),

    path('product/all', ProductListView.as_view(), name='product-all'),
    path('product/add', ProductCreateView.as_view(), name='product-add'),

]
