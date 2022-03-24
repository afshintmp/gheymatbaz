from django.contrib import admin
from shop.models import Product, Category, Brand, CategoryAttribute, CategoryAttributeValue


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


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'category']
    list_filter = ['brand', 'category']
    search_fields = ['title', 'category__name', 'brand__name']



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
