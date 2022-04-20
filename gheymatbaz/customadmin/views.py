from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from customadmin.forms import AddCategoryForm, EditeCategory, CategoryAttributeValueForm
from customadmin.utils import check_is_superuser
from shop.models import Category, Product, Brand, CategoryAttribute, CategoryAttributeValue


# Create your views here.
@login_required(login_url='/gheymat-admin/authenticate')
@require_http_methods(request_method_list=['GET'])
@user_passes_test(check_is_superuser)
def admin_panel(request):
    return HttpResponse("welcome to admin panel")


def admin_authenticate(request):
    context = dict()
    logout(request)
    username = password = redirect = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        redirect = request.POST['next']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect)
        else:
            context['error'] = 'خطا در احراز هویت'

    try:
        context['next'] = request.GET['next']
    except MultiValueDictKeyError:
        context['next'] = request.POST['next']
    except:
        context['next'] = 'gheymat-admin'

    return render(request, "customadmin/login-template.html", context=context)


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
    fields = ['title', 'slug', 'status', 'image', 'brand', 'category']
    template_name = 'customadmin/create-product.html'
    success_url = reverse_lazy('product-all')

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['title', 'slug', 'status', 'image', 'brand', 'category']
    template_name = 'customadmin/create-product.html'
    success_url = reverse_lazy('product-all')

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def product_advanced_update(request, pk):
    if request.method == "POST":
        form = request.POST
        product = Product.objects.get(pk=pk)
        attribute_dict = list()
        for f in form:
            if not f == 'csrfmiddlewaretoken':
                attribute_dict.append(form[f])

        product.category_attribute_value.clear()
        product.category_attribute_value.set(attribute_dict)

        return render(request, "customadmin/trace.html", context=form)

    else:

        context = dict()

        product = Product.objects.get(pk=pk)
        category = product.category.all()
        category_attribute = CategoryAttribute.objects.filter(category_id__in=category)
        category_attribute_value = CategoryAttributeValue.objects.filter(category_attribute_id__in=category_attribute)

        context['products'] = product
        context['categoryattribute'] = category_attribute
        context['categoryattributevalue'] = category_attribute_value

        return render(request, "customadmin/product-advanced-update.html", context=context)


class CategoryAttributeCreateView(CreateView):
    model = CategoryAttribute
    fields = ['name', 'category', 'slug']
    template_name = 'customadmin/edit-category-attribute.html'
    success_url = reverse_lazy('category-attribute-add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoryattribute = CategoryAttribute.objects.all()
        context['object_list'] = categoryattribute
        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoryAttributeUpdateView(UpdateView):
    model = CategoryAttribute
    fields = ['name', 'category', 'slug']
    template_name = 'customadmin/edit-category-attribute.html'
    success_url = reverse_lazy('category-attribute-add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoryattribute = CategoryAttribute.objects.all()
        context['object_list'] = categoryattribute
        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoryAttributeDeleteView(DeleteView):
    model = CategoryAttribute
    success_url = reverse_lazy('category-attribute-add')
    template_name = 'customadmin/confirm-delete-category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['categories'] = category
        context['json_categories'] = serializers.serialize('json', category)
        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def category_attribute_value(request, pk):
    if request.method == "POST":
        form = request.POST
        category_attribute = CategoryAttribute.objects.get(pk=form['parent_attribute_id'])
        c = CategoryAttributeValue(attribute_value=form['attribute_value'],
                                   category_attribute=category_attribute)
        c.save()
        context = dict()
        context['object_list'] = CategoryAttributeValue.objects.filter(category_attribute=pk)
        context['form'] = CategoryAttributeValueForm({'parent_attribute_id': pk})
        return render(request, 'customadmin/edit-category-attribute-value.html', context=context)



    else:

        context = dict()
        context['object_list'] = CategoryAttributeValue.objects.filter(category_attribute=pk)
        context['form'] = CategoryAttributeValueForm({'parent_attribute_id': pk})
        return render(request, 'customadmin/edit-category-attribute-value.html', context=context)

# template_name = 'customadmin/edit-category-attribute-value.html'
