from django.urls import path, re_path
from customadmin.views import edit_product, CategoryCreateView, \
    CategoryUpdateView, CategoryDeleteView, BrandCreateView, BrandUpdateView, BrandDeleteView, ProductListView, \
    ProductCreateView, ProductUpdateView, product_advanced_update, CategoryAttributeCreateView, \
    CategoryAttributeUpdateView, CategoryAttributeDeleteView, category_attribute_value

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
    path('product/<int:pk>', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/advanced', product_advanced_update, name='product-advanced-update'),

    path('category-attribute/add/', CategoryAttributeCreateView.as_view(), name='category-attribute-add'),
    path('category-attribute/<int:pk>/', CategoryAttributeUpdateView.as_view(), name='category-attribute-update'),
    path('category-attribute/<int:pk>/delete/', CategoryAttributeDeleteView.as_view(),
         name='category-attribute-delete'),

    path('category-attribute-value/<int:pk>/', category_attribute_value,
         name='category-attribute-value-list')
]
