import json

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from django.core.validators import slug_unicode_re
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from customadmin.forms import CategoryAttributeValueForm
from customadmin.utils import check_is_superuser
from shop.models import Category, Product, Brand, CategoryAttribute, CategoryAttributeValue, \
    ProductCategoryAttributeValue, ProductRelation, ProductGallery, ProductKeyWord, ProductAttribute, CategoryMeta, \
    GlobalAttribute, ProductGlobalAttribute


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
def category_create_view(request):
    context = dict()
    if request.method == "POST":
        form = request.POST
        if Category.objects.filter(slug=form.get('slug')).exists():
            context['rise_error'] = 'اسلاگ برای دسته بندیه دیگری استفاده شده'
        else:
            if slug_unicode_re.match(form.get('slug')):
                c = Category(name=form.get('name'),
                             parent_id=form.get('parent'),
                             slug=form.get('slug'),
                             icon_class=form.get('icon-class'))
                c.save()
            else:
                context['rise_error'] = 'اسلاگ غیر معتبر'

    category = Category.objects.all()

    context['category'] = category

    return render(request, "customadmin/edit-category.html", context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def category_edit_view(request, pk):
    context = dict()
    category = Category.objects.all()
    context['category'] = category
    context['current_category'] = current_category = category.get(pk=pk)
    if request.method == "POST":
        form = request.POST
        if current_category.slug != form.get('slug') and Category.objects.filter(slug=form.get('slug')).exists():
            context['rise_error'] = 'اسلاگ برای دسته بندیه دیگری استفاده شده'
        else:
            if slug_unicode_re.match(form.get('slug')):
                current_category.name = form.get('name')
                if form.get('parent') == '':
                    pass
                else:
                    current_category.parent = category.get(pk=form.get('parent'))

                current_category.slug = form.get('slug')
                current_category.icon_class = form.get('icon-class')
                current_category.save()
                return redirect(category_create_view)
            else:
                context['rise_error'] = 'اسلاگ غیر معتبر'

    return render(request, "customadmin/edit-category.html", context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def category_advanced_view(request, pk):
    context = dict()
    context['current_category'] = current_category = Category.objects.get(pk=pk)

    context['category_child_list'] = category_child_list = current_category.get_child()
    context['category_attribute'] = category_attribute = CategoryAttribute.objects.filter(
        category__in=category_child_list)

    context['brand'] = brand = Product.objects.values_list('brand', 'brand__name', 'brand__image',
                                                           'brand__slug').distinct()
    if request.method == "POST":
        form = request.POST
        cat_filter = json.dumps(form.getlist('filter[]'))
        spe_brand = json.dumps(form.getlist('brands[]'))
        description = form.get('description')
        meta_title = form.get('meta_title')
        meta_description = form.get('meta_description')
        noindex = form.get('noindex')
        if noindex is not None:
            index_status = True
        else:
            index_status = False

        f = CategoryMeta.objects.update_or_create(
            category=current_category,
            defaults={'filter': cat_filter, 'special_brand': spe_brand, 'description': description,
                      'meta_title': meta_title, 'meta_description': meta_description, 'noindex': index_status},
        )
        return redirect('category-add')
    try:
        category_meta = CategoryMeta.objects.get(category=current_category)
        context['category_meta_filter'] = json.loads(category_meta.filter)
        context['category_meta_special_brand'] = json.loads(category_meta.special_brand)
        context['category_meta_description'] = category_meta.description
        context['meta_title'] = category_meta.meta_title
        context['meta_description'] = category_meta.meta_description
        context['noindex'] = category_meta.noindex
        context['current_category_attribute'] = current_category_attribute = CategoryAttribute.objects.filter(
            category__in=json.loads(category_meta.filter))
        context['current_category_special_brand'] = current_category_special_brand = Brand.objects.filter(
            pk__in=json.loads(category_meta.special_brand))
    except:
        category_meta = ''
    return render(request, 'customadmin/edit-category-advanced.html', context=context)


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('author-list')
    template_name = 'customadmin/confirm-delete-category.html'
    success_url = reverse_lazy('category-add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['category'] = category
        context['json_categories'] = serializers.serialize('json', category)
        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def brand_add_view(request):
    context = dict()
    if request.method == "POST":
        form = request.POST
        form_file = request.FILES
        if Brand.objects.filter(slug=form.get('slug')).exists():
            context['rise_error'] = 'اسلاگ برای برند دیگری استفاده شده'
        else:
            if slug_unicode_re.match(form.get('slug')):
                c = Brand(name=form.get('title'),

                          slug=form.get('slug'),
                          image=form_file.get('pic'))
                c.save()
                return redirect(brand_add_view)
            else:
                context['rise_error'] = 'اسلاگ غیر معتبر'

    brand = Brand.objects.all()
    context['brands'] = brand
    context['is_new'] = True
    return render(request, "customadmin/edit-brand.html", context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def brand_update_view(request, pk):
    context = dict()
    context['current_brand'] = current_brand = Brand.objects.get(pk=pk)
    if request.method == "POST":
        form = request.POST
        form_file = request.FILES
        if current_brand.slug != form.get('slug') and Brand.objects.filter(slug=form.get('slug')).exists():
            context['rise_error'] = 'اسلاگ برای برند دیگری استفاده شده'
        else:
            if slug_unicode_re.match(form.get('slug')):
                current_brand.name = form.get('title')
                current_brand.slug = form.get('slug')
                if form_file.get('pic') is not None:
                    current_brand.image = form_file.get('pic')
                current_brand.save()
                return redirect(brand_add_view)
            else:
                context['rise_error'] = 'اسلاگ غیر معتبر'

    brand = Brand.objects.all()
    context['brands'] = brand
    return render(request, "customadmin/edit-brand.html", context=context)





class BrandDeleteView(DeleteView):
    model = Brand
    success_url = reverse_lazy('author-list')
    template_name = 'customadmin/confirm-delete-brand.html'
    success_url = reverse_lazy('category-add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.objects.all()
        context['brands'] = brand

        return context

    @method_decorator(login_required, user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'customadmin/confirm-delete-product.html'
    success_url = reverse_lazy('product-all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.all()
        context['products'] = product
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


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def product_update(request, pk):
    product = Product.objects.get(pk=pk)

    if request.method == "POST":
        form = request.POST

        form_file = request.FILES
        product.title = form['title']
        product.en_title = form['en-title']
        product.slug = form['slug']
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
        return redirect(product_advanced_update, product.pk)

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

        product = Product(title=form['title'],
                          en_title=form['en-title'],
                          description=form['context'],
                          meta_title=form['meta_title'],
                          meta_description=form['meta_description'],
                          slug=form['slug']

                          )

        product.save()

        return redirect(product_advanced_update, product.pk)

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

    product_global_attribute = ProductGlobalAttribute.objects.filter(product_id=product)

    if request.method == "POST":
        form = request.POST
        form_file = request.FILES
        alt_text = form.getlist('alt_text[]')
        alt_text_edit = form.getlist('alt_text_edit[]')
        keyword = form.getlist('keyword[]')
        global_attribute = form.getlist('global_attr[]')
        product_global_attribute.delete()
        if global_attribute is not None:
            ga = ProductGlobalAttribute.objects.create(product_id=product)
            ga.global_attribute.set(global_attribute)
            ga.save()
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
        special = form.getlist('attr[][spe]')

        ProductAttribute.objects.filter(product_id=product).delete()
        if pro_attr_name is not None:

            attr_dict = dict(zip(pro_attr_name, form.getlist('attr[][val]')))
            i = 0
            for atr in attr_dict:
                if special[i] == 'true':
                    spe = True
                else:
                    spe = False
                ata = ProductAttribute(product_id=product,
                                       attribute=atr,
                                       attribute_value=attr_dict[atr],
                                       in_header=spe)

                ata.save()
                i = i + 1
        product.status = form['status']
        product.save()

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
    context['global_attribute'] = GlobalAttribute.objects.all()
    return render(request, "customadmin/product-advanced-update.html", context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def category_attribute_create_view(request, pk):
    context = dict()
    context['all_category'] = all_category = Category.objects.filter(child_category_list__isnull=True)
    if request.method == "POST":
        form = request.POST
        if CategoryAttribute.objects.filter(slug=form.get('slug')).exists() and form.get('slug') is not None:
            context['rise_error'] = 'اسلاگ برای دسته بندیه دیگری استفاده شده'
        else:
            if slug_unicode_re.match(form.get('slug')):
                ca = CategoryAttribute.objects.create(name=form.get('name')
                                                      , category_id=form.get('category_id')
                                                      , slug=form.get('slug'))
                ca.save()
            else:
                context['rise_error'] = 'اسلاگ غیر معتبر'

    context['category'] = category = all_category.get(pk=pk)
    context['category_attribute'] = CategoryAttribute.objects.filter(category_id=category)

    return render(request, 'customadmin/edit-category-attribute.html', context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def attribute_create_view(request):
    context = dict()
    context['category'] = Category.objects.filter(child_category_list__isnull=True)
    if request.method == "POST":
        form = request.POST
        if CategoryAttribute.objects.filter(slug=form.get('slug')).exists() and form.get('slug') is not None:
            context['rise_error'] = 'اسلاگ برای دسته بندیه دیگری استفاده شده'
        else:
            if slug_unicode_re.match(form.get('slug')):
                ca = CategoryAttribute.objects.create(name=form.get('name')
                                                      , category_id=form.get('category_id')
                                                      , slug=form.get('slug'))
                ca.save()
            else:
                context['rise_error'] = 'اسلاگ غیر معتبر'

    context['category_attribute'] = CategoryAttribute.objects.all()
    return render(request, 'customadmin/edit-attribute.html', context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def attribute_update_view(request, pk):
    context = dict()
    context['category'] = Category.objects.filter(child_category_list__isnull=True)
    context['category_attribute'] = category_attribute = CategoryAttribute.objects.all()
    context['current_category_attribute'] = current_category_attribute = category_attribute.get(pk=pk)
    if request.method == "POST":
        form = request.POST
        if CategoryAttribute.objects.filter(slug=form.get('slug')).exists() and \
                form.get('slug') is not None and \
                form.get('slug') != current_category_attribute.slug:
            context['rise_error'] = 'اسلاگ برای دسته بندیه دیگری استفاده شده'
        else:
            if slug_unicode_re.match(form.get('slug')):
                current_category_attribute.name = form.get('name')
                current_category_attribute.category_id = form.get('category_id')
                current_category_attribute.slug = form.get('slug')
                current_category_attribute.save()
            else:
                context['rise_error'] = 'اسلاگ غیر معتبر'

    context['category_attribute'] = CategoryAttribute.objects.all()

    return render(request, 'customadmin/update-attribute.html', context=context)


def category_attribute_delete_view(request, pk):
    context = dict()
    context['product_list_id'] = product_list_id = ProductCategoryAttributeValue.objects.filter(
        category_attribute=pk).values_list(
        'product_id', flat=True)
    context['products'] = Product.objects.filter(pk__in=product_list_id)
    if request.method == "POST":
        form = request.POST
        category_attribute = CategoryAttribute.objects.get(pk=pk)
        if category_attribute is not None:
            category_attribute.delete()
        response = redirect('/gheymat-admin/category-attribute/add')
        return response

    return render(request, 'customadmin/confirm-delete-category-attribute.html', context=context)


class CategoryAttributeDeleteView(DeleteView):
    model = CategoryAttribute
    success_url = reverse_lazy('attribute-add')
    template_name = 'customadmin/confirm-delete-category-attribute.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_attribute = CategoryAttribute.objects.all()
        context['category_attribute'] = category_attribute
        context['category'] = Category.objects.filter(child_category_list__isnull=True)
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
    context['category_attribute'] = CategoryAttribute.objects.get(pk=pk)
    context['form'] = CategoryAttributeValueForm({'parent_attribute_id': pk})
    return render(request, 'customadmin/edit-category-attribute-value.html', context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def category_attribute_value_add(request, pk):
    if request.method == "POST":
        form = request.POST
        category_attribute = CategoryAttribute.objects.get(pk=pk)
        c = CategoryAttributeValue(attribute_value=form.get('attribute_value'),
                                   category_attribute=category_attribute)
        c.save()

    context = dict()
    context['object_list'] = CategoryAttributeValue.objects.filter(category_attribute=pk)
    context['category_attribute'] = CategoryAttribute.objects.get(pk=pk)

    return render(request, 'customadmin/add-category-attribute-value.html', context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def category_attribute_value_edit(request, pk):
    category_attribute_value = CategoryAttributeValue.objects.get(pk=pk)
    parent = category_attribute_value.category_attribute.pk
    if request.method == "POST":
        form = request.POST

        category_attribute_value.attribute_value = form.get('attribute_value')
        category_attribute_value.save()

        return redirect('category-attribute-value-add', pk=parent)

    context = dict()
    context['category_attribute_value'] = CategoryAttributeValue.objects.get(pk=pk)
    context['object_list'] = CategoryAttributeValue.objects.filter(
        category_attribute=category_attribute_value.category_attribute)
    context['category_attribute'] = CategoryAttribute.objects.get(pk=category_attribute_value.category_attribute.pk)

    return render(request, 'customadmin/edit-category-attribute-value.html', context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def category_attribute_value_delete(request, pk):
    category_attribute_value = CategoryAttributeValue.objects.get(pk=pk)
    parent = category_attribute_value.category_attribute.pk
    if request.method == "POST":
        form = request.POST
        category_attribute_value.delete()
        return redirect('category-attribute-value-add', pk=parent)

    context = dict()
    context['category_attribute_value'] = CategoryAttributeValue.objects.get(pk=pk)
    context['object_list'] = CategoryAttributeValue.objects.filter(
        category_attribute=category_attribute_value.category_attribute)
    context['category_attribute'] = CategoryAttribute.objects.get(pk=parent)

    return render(request, 'customadmin/confirm-delete-category-attribute-value.html', context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def global_attribute_add(request):
    if request.method == "POST":
        form = request.POST
        name = form['name']
        color_code = form['color-code']
        ga = GlobalAttribute.objects.create(title=name
                                            , color_code=color_code
                                            )
        ga.save()
    context = dict()
    context['object'] = GlobalAttribute.objects.all()
    return render(request, 'customadmin/global-attribute.html', context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def global_attribute_delete(request, pk):
    if request.method == "POST":
        form = request.POST

        ga = GlobalAttribute.objects.get(pk=pk)
        ga.delete()
        return redirect('global-attribute-add')
    context = dict()
    context['object'] = GlobalAttribute.objects.get(pk=pk)
    context['global_attribute'] = GlobalAttribute.objects.all()
    return render(request, 'customadmin/confirm-delete-global-attribute.html', context=context)


@login_required(login_url='/admin/login')
@require_http_methods(request_method_list=['GET', 'POST'])
@user_passes_test(check_is_superuser)
def global_attribute_update(request, pk):
    if request.method == "POST":
        form = request.POST
        name = form['name']
        color_code = form['color-code']
        ga = GlobalAttribute.objects.get(pk=pk)
        ga.title = name
        ga.color_code = color_code
        ga.save()
        return redirect('global-attribute-add')
    context = dict()
    context['current_attribute'] = GlobalAttribute.objects.get(pk=pk)
    context['object'] = GlobalAttribute.objects.all()
    return render(request, 'customadmin/global-attribute.html', context=context)
