from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods

from shop.models import Product, Category


@require_http_methods(request_method_list=['GET'])
def single_product(request, slug):
    context = dict()
    context['product'] = Product.objects.get(slug=slug)
    return render(request, "shop/single-product.html", context=context)


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
