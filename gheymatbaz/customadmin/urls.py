from django.urls import path, re_path
from customadmin.views import CategoryDeleteView, BrandDeleteView, ProductListView, \
    product_advanced_update, ProductDeleteView, \
    CategoryAttributeDeleteView, category_attribute_value, admin_panel, admin_authenticate, \
    product_update, product_add, category_create_view, category_edit_view, category_advanced_view, \
    category_attribute_create_view, attribute_create_view, attribute_update_view, category_attribute_value_add, \
    category_attribute_value_delete, category_attribute_value_edit, category_attribute_delete_view, \
    global_attribute_add, global_attribute_delete, global_attribute_update, brand_add_view, brand_update_view

urlpatterns = [
    path('', admin_panel, name='admin-panel'),
    path('authenticate', admin_authenticate),

    path('category/add', category_create_view, name='category-add'),
    path('category/<int:pk>', category_edit_view, name='category-update'),
    path('category/<int:pk>/advaced', category_advanced_view, name='category-advanced'),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),
    path('brand/add', brand_add_view, name='brand-add'),
    # path('brand/add', BrandCreateView.as_view(), name='brand-add'),
    path('brand/<int:pk>', brand_update_view, name='brand-update'),
    path('brand/<int:pk>/delete', BrandDeleteView.as_view(), name='brand-delete'),

    path('product/all', ProductListView.as_view(), name='product-all'),
    path('product/add', product_add, name='product-add'),
    path('product/<int:pk>', product_update, name='product-update'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
    path('product/<int:pk>/advanced', product_advanced_update, name='product-advanced-update'),

    path('category-attribute/add', attribute_create_view, name='attribute-add'),
    path('category/<int:pk>/category-attribute/add', category_attribute_create_view, name='category-attribute-add'),
    path('category-attribute/<int:pk>', attribute_update_view, name='category-attribute-update'),
    path('category-attribute/<int:pk>/delete', category_attribute_delete_view,
         name='category-attribute-delete'),

    path('category-attribute-value/<int:pk>/add', category_attribute_value_add,
         name='category-attribute-value-add'),
    path('category-attribute-value/edit/<int:pk>/', category_attribute_value_edit,
         name='category-attribute-value-edit'),
    path('category-attribute-value/delete/<int:pk>/', category_attribute_value_delete,
         name='category-attribute-value-delete'),

    path('global-attribute/add', global_attribute_add, name='global-attribute-add'),
    path('global-attribute/<int:pk>/edit', global_attribute_update, name='global-attribute-update'),
    path('global-attribute/<int:pk>/delete', global_attribute_delete, name='global-attribute-delete'),
]
