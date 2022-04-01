from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from customadmin.forms import AddCategoryForm, EditeCategory
from customadmin.utils import check_is_superuser
from shop.models import Category, Product, Brand, CategoryAttribute, CategoryAttributeValue


# Create your views here.

@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET'])
@user_passes_test(check_is_superuser)
def all_product(request):
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
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def all_category(request):
    form = AddCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
    categories = Category.objects.all()
    data_categories = serializers.serialize('json', categories)

    return render(request, "customadmin/all-category.html", {'categories': categories,
                                                             'json_categories': data_categories,
                                                             'form': AddCategoryForm
                                                             })


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def edit_category(request, pk):
    if request.method == 'POST':
        form = EditeCategory(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
    query = Category.objects.filter(pk=pk).first()
    # if query.exists():
    form = EditeCategory()
    categories = Category.objects.all()
    data_categories = serializers.serialize('json', categories)

    return render(request, "customadmin/edit-category.html", {'current_category': query,
                                                              'categories': categories,
                                                              'json_categories': data_categories,
                                                              'form': form
                                                              })
