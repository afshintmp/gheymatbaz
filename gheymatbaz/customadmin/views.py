from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from customadmin.forms import AddProductForm
from customadmin.utils import check_is_superuser
from shop.models import Category, Product, Brand, CategoryAttribute, CategoryAttributeValue

import json


# Create your views here.

@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET'])
@user_passes_test(check_is_superuser)
def admin_product(request):
    context = dict()
    context['products'] = Product.objects.all()
    return render(request, "customadmin/all-product.html", context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET'])
@user_passes_test(check_is_superuser)
def edit_product(request):
    context = dict()
    context['products'] = Product.objects.all()
    return HttpResponse('edit product')


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET'])
@user_passes_test(check_is_superuser)
def add_product(request):
    context = dict()
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    category_attribute = CategoryAttribute.objects.all()
    category_attribute_value = CategoryAttributeValue.objects.all()

    data_categories = serializers.serialize('json', categories)
    data_category_attribute = serializers.serialize('json', category_attribute)
    data_category_attribute_value = serializers.serialize('json', category_attribute_value)
    # context['form'] = AddProductForm

    # return HttpResponse(data, content_type="application/json")
    return render(request, "customadmin/insert-product.html", {'brands': brands,
                                                               'categories': categories,
                                                               'json_categories': data_categories,
                                                               'json_category_attribute': data_category_attribute,
                                                               'json_category_attribute_value': data_category_attribute_value
                                                               })


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['post'])
@user_passes_test(check_is_superuser)
def create_product(request):
    context = dict()
    context['products'] = Product.objects.all()
    return render(request, "customadmin/insert-product.html", context=context)
