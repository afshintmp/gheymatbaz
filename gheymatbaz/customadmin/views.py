from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from customadmin.utils import check_is_superuser
from shop.models import Category, Product


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
    context['products'] = Product.objects.all()
    return HttpResponse('add product')
