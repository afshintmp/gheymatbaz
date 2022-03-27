from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods

from shop.models import Product


@require_http_methods(request_method_list=['GET'])
def single_product(request, slug):
    context = dict()
    context['product'] = Product.objects.get(slug=slug)
    return render(request, "shop/single-product.html", context=context)


def list_all(request):
    context = dict()
    context['products'] = Product.objects.all()
    return render(request, "shop/archive-product.html", context=context)
