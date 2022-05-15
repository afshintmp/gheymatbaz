from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods

from shop.models import Product, Category, ProductCategoryAttributeValue, CategoryAttribute, ProductRelation, \
    ProductGallery


# @require_http_methods(request_method_list=['GET'])
def single_product(request, slug):
    context = dict()
    product = Product.objects.get(slug=slug)
    product_category_attribute = ProductCategoryAttributeValue.objects.filter(product_id=product.pk)
    category_attribute = CategoryAttribute.objects.filter(category_id__in=product.category.all()).prefetch_related(
        'related_category_attribute')
    product.view = product.view + 1
    product.save()
    context['product'] = product
    context['product_category_attribute'] = product_category_attribute
    context['category_attribute'] = category_attribute
    context['product_rel'] = ProductRelation.objects.filter(product=product)
    context['product_gallery'] = ProductGallery.objects.filter(product_id=product)
    html = render(request, "shop/single-product.html", context=context)

    return html


def list_all(request):
    context = dict()
    context['products'] = Product.objects.all()

    return render(request, "shop/archive-product.html", context=context)


def category_list(request, slug):
    context = dict()
    context['products'] = Product.objects.all()
    return render(request, "shop/archive-product.html", context=context)


def index(request):
    context = dict()
    context['categories'] = Category.objects.all()
    return render(request, "index.html", context=context)


def single_brand(request, slug):
    pass
