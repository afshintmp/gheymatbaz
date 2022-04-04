from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

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


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'parent', 'slug']
    template_name = 'customadmin/edit-category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['categories'] = category
        context['json_categories'] = serializers.serialize('json', category)
        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'parent', 'slug']
    template_name = 'customadmin/edit-category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['categories'] = category
        context['json_categories'] = serializers.serialize('json', category)
        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('author-list')
    template_name = 'customadmin/confirm-delete-category.html'
    success_url = reverse_lazy('category-add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['categories'] = category
        context['json_categories'] = serializers.serialize('json', category)
        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BrandCreateView(CreateView):
    model = Brand
    fields = ['name', 'slug', 'image']
    template_name = 'customadmin/edit-brand.html'
    success_url = reverse_lazy('brand-add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.objects.all()
        context['brands'] = brand
        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BrandUpdateView(UpdateView):
    model = Brand
    fields = ['name', 'slug', 'image', 'brand', 'category']
    template_name = 'customadmin/edit-brand.html'
    success_url = reverse_lazy('brand-add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.objects.all()
        context['brands'] = brand

        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BrandDeleteView(DeleteView):
    model = Brand
    success_url = reverse_lazy('author-list')
    template_name = 'customadmin/confirm-delete-category.html'
    success_url = reverse_lazy('category-add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['categories'] = category
        context['json_categories'] = serializers.serialize('json', category)
        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductListView(ListView):
    model = Product
    template_name = 'customadmin/all-product.html'

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    fields = ['title', 'slug', 'status', 'brand', 'category', 'category_attribute_value']
    template_name = 'customadmin/create-product.html'
    success_url = reverse_lazy('product-all')

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
