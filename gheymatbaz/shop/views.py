from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods


@require_http_methods(request_method_list=['GET'])
def single_product(request):
    context = dict()
    return render(request, "shop/single-product.html", context=context)
