import os

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from customadmin.forms import AddCategoryForm, EditeCategory, CategoryAttributeValueForm
from customadmin.utils import check_is_superuser
from gheymatbaz import settings
from shop.models import Category, Product, Brand, CategoryAttribute, CategoryAttributeValue, \
    ProductCategoryAttributeValue, ProductRelation, ProductGallery, ProductKeyWord, ProductAttribute


# Create your views here.
@login_required(login_url='/gheymat-admin/authenticate')
@require_http_methods(request_method_list=['GET'])
@user_passes_test(check_is_superuser)
def admin_panel(request):
    return render(request, "customadmin/admin-index.html", context={})


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
        try:
            context['next'] = request.POST['next']
        except MultiValueDictKeyError:
            context['next'] = '/gheymat-admin'

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
    fields = ['name', 'parent', 'slug', 'icon_class']
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
    fields = ['name', 'parent', 'slug', 'icon_class']
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
    fields = ['title', 'slug', 'status', 'image', 'alt_text', 'brand', 'category']
    template_name = 'customadmin/create-product.html'
    success_url = reverse_lazy('product-all')

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def product_update(request, pk):
    product = Product.objects.get(pk=pk)

    if request.method == "POST":
        form = request.POST

        form_file = request.FILES
        product.title = form['title']
        product.description = form['context']
        product.meta_title = form['meta_title']
        product.meta_description = form['meta_description']

        if form.getlist("category") is not None:
            # category_obj = Category.objects.filter(id__in=form.getlist('category'))
            product.category.set(form.getlist('category'))

        if form.get("brand") != '0':
            brand_obj = Brand.objects.get(pk=form['brand'])
            product.brand = brand_obj
        else:
            product.brand = None

        if form_file.get("pic") is not None:
            product.image = form_file['pic']

        if form.get("alt-text") is not None:
            product.alt_text = form['alt-text']
        else:
            product.alt_text = None

        if form.get("removeimage") is not None:
            product.image = None
            product.alt_text = None

        if form.get("noindex") is not None:
            product.noindex = True
        else:
            product.noindex = False

        product.save()

    context = dict()
    context['product'] = product
    context['category'] = Category.objects.all()
    context['brand'] = Brand.objects.all()
    return render(request, "customadmin/create-product-custom.html", context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def product_add(request):
    if request.method == "POST":
        form = request.POST
        # product = Product.objects.get(pk=pk)

        product = Product(title=form['title'],
                          description=form['context'],
                          meta_title=form['meta_title'],
                          meta_description=form['meta_description'],
                          slug=form['slug']

                          )

        product.save()

        return render(request, "customadmin/trace.html", context=form)

    context = dict()
    context['category'] = Category.objects.all()
    context['brand'] = Brand.objects.all()
    return render(request, "customadmin/create-product-custom.html", context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def product_advanced_update(request, pk):
    product = Product.objects.get(pk=pk)

    product_category_attribute_value = ProductCategoryAttributeValue.objects.filter(
        product_id=product)
    product_relation = ProductRelation.objects.filter(product=product)
    product_keyword = ProductKeyWord.objects.filter(product_id=product)
    if request.method == "POST":
        form = request.POST
        form_file = request.FILES
        alt_text = form.getlist('alt_text[]')
        alt_text_edit = form.getlist('alt_text_edit[]')
        keyword = form.getlist('keyword[]')
        product_keyword.delete()
        if keyword is not None:

            for k in keyword:
                keyword = ProductKeyWord(keyword=k,
                                         product_id=product)

                keyword.save()

        if alt_text_edit is not None:
            gallery_dict = dict(zip(form.getlist('gallery_pic[]'), alt_text_edit))
            for g in gallery_dict:
                pic_gallery = ProductGallery.objects.get(pk=g)
                pic_gallery.alt_text = gallery_dict[g]
                pic_gallery.save()

        if form_file.getlist('pic') is not None:
            pic_dict = dict(zip(form_file.getlist('pic'), alt_text))
            for p in pic_dict:
                g = ProductGallery(image=p,
                                   alt_text=pic_dict[p],
                                   product_id=product)
                g.save()

        cats = form.getlist('attribute[]')
        rel_name = form.getlist('rel[][name]')
        if rel_name:
            product_relation.delete()
            rel_product = form.getlist('rel[][product]')
            rel_dict = dict(zip(rel_name, rel_product))

            for rd in rel_dict:
                product_rel = Product.objects.get(pk=rel_dict[rd])
                r = ProductRelation(title=rd,
                                    product=product,
                                    product_rel=product_rel
                                    )
                r.save()

        if form.getlist("alttextedit[]") is not None:
            alt_text = form.getlist("alttextedit[]")
            for alt in alt_text:
                if alt:
                    a = ProductGallery.objects.filter(product_id=product)
                    a.alt_text = alt
                    a.save()

        product_category_attribute_value.delete()

        for cat in cats:
            if cat:
                category_attribute_value_obj = CategoryAttributeValue.objects.get(pk=cat)

                p = ProductCategoryAttributeValue(product_id=product,
                                                  category_attribute=category_attribute_value_obj.category_attribute,
                                                  category_attribute_value=category_attribute_value_obj)
                if form.get(str(category_attribute_value_obj.category_attribute.pk)) is not None:
                    p.in_header = True
                else:
                    p.in_header = False

                p.save()

        pro_attr_name = form.getlist('attr[][title]')
        ProductAttribute.objects.filter(product_id=product).delete()
        if pro_attr_name is not None:

            attr_dict = dict(zip(pro_attr_name, form.getlist('attr[][val]')))
            for atr in attr_dict:
                ata = ProductAttribute(product_id=product,
                                       attribute=atr,
                                       attribute_value=attr_dict[atr])

                ata.save()

    context = dict()

    category = product.category.all()

    category_product = Product.objects.filter(category__in=category)
    category_attribute = CategoryAttribute.objects.filter(category_id__in=category).prefetch_related(
        'related_category_attribute')

    category_attribute_value = CategoryAttributeValue.objects.filter(
        category_attribute_id__in=category_attribute)

    context['product'] = product
    context['category_product'] = category_product
    context['categoryattribute'] = category_attribute
    context['categoryattributevalue'] = category_attribute_value
    context['productcategoryattributevalue'] = product_category_attribute_value
    context['product_rel'] = ProductRelation.objects.filter(product=product)
    context['product_keyword'] = ProductKeyWord.objects.filter(product_id=product)
    context['product_gallery'] = ProductGallery.objects.filter(product_id=product).order_by('id')
    context['pro_attribute'] = ProductAttribute.objects.filter(product_id=product)
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
