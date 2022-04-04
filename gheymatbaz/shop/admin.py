from django.contrib import admin
from shop.models import Product, Category, Brand, CategoryAttribute, CategoryAttributeValue, ProductGallery, \
    ProductKeyWord, ProductAttribute


# Register your models here.
class ProductInline(admin.TabularInline):
    model = CategoryAttribute
    extra = 1


class CategoryAttributeInline(admin.TabularInline):
    model = CategoryAttribute
    extra = 1


class CategoryAttributeValueInline(admin.TabularInline):
    model = CategoryAttributeValue
    extra = 1


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery


class ProductKeywordInline(admin.TabularInline):
    model = ProductKeyWord


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand']
    list_filter = ['brand', 'category']
    search_fields = ['title', 'category__name', 'brand__name']
    inlines = [ProductGalleryInline, ProductKeywordInline, ProductAttributeInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', ]
    inlines = [CategoryAttributeInline]


class CategoryAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', ]
    list_filter = ['category']
    inlines = [CategoryAttributeValueInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(CategoryAttribute, CategoryAttributeAdmin)
