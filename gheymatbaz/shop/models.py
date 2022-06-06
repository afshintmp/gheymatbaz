from itertools import chain

from django.db import models
from django.urls import reverse

# Create your models here.
from shop.utils import get_child_id_func


class ProductKeyWord(models.Model):
    keyword = models.CharField(max_length=32, blank=False, null=False)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword


class Brand(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    slug = models.SlugField(max_length=200, allow_unicode=True, null=False, blank=False, unique=True)
    image = models.ImageField(upload_to='brand', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand-add', args=[self.slug])

    @property
    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return ""


class Category(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True,
                               related_name='child_category_list', )
    slug = models.SlugField(max_length=200, allow_unicode=True, null=False, blank=False, unique=True)
    icon_class = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'categories'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('category-archive', args=[self.slug])

    def get_child(self):
        a = self.child_category_list.all()
        for cat in a:
            a = list(chain(a, cat.child_category_list.all()))
        for cat in a:
            a = list(chain(a, cat.child_category_list.all()))
        for cat in a:
            a = list(chain(a, cat.child_category_list.all()))
        for cat in a:
            a = list(chain(a, cat.child_category_list.all()))
        for cat in a:
            a = list(chain(a, cat.child_category_list.all()))
        for cat in a:
            a = list(chain(a, cat.child_category_list.all()))
        for cat in a:
            a = list(chain(a, cat.child_category_list.all()))
        return set(a)


class CategoryMeta(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, unique=True)
    filter = models.JSONField(max_length=800, null=True, blank=True)
    special_brand = models.JSONField(max_length=800, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category.name


class CategoryAttribute(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, name='category',
                                    related_name='related_category')
    slug = models.SlugField(max_length=200, allow_unicode=True, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class CategoryAttributeValue(models.Model):
    attribute_value = models.CharField(max_length=32, null=False, blank=False)
    parent_attribute_id = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE, name='category_attribute',
                                            related_name='related_category_attribute')

    def __str__(self):
        return self.attribute_value


class Product(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=400, blank=False, null=False)

    published_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='published')

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True)

    category = models.ManyToManyField(Category, blank=True)

    view = models.BigIntegerField(default=0)
    rate = models.BigIntegerField(default=0)
    rate_number = models.BigIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product', null=True, blank=True)
    alt_text = models.CharField(max_length=200, null=True, blank=True)

    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.CharField(max_length=300, null=True, blank=True)
    noindex = models.BooleanField(null=False, blank=True, default=False)
    slug = models.SlugField(max_length=200, allow_unicode=True, null=False, blank=False, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single-product', args=[self.slug])

    def get_add_product_url(self):
        return reverse('admin-add-product', args=[self.slug])

    @property
    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return ""


class ProductCategoryAttributeValue(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    category_attribute = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE)
    category_attribute_value = models.ForeignKey(CategoryAttributeValue, on_delete=models.CASCADE,
                                                 name='category_attribute_value',
                                                 related_name='related_category_attribute_value')
    in_header = models.BooleanField(default=False)

    def __str__(self):
        return self.category_attribute_value.attribute_value


class ProductGallery(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    image = models.ImageField(upload_to='product_image', null=False, blank=False)
    alt_text = models.CharField(max_length=200, null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True)


class ProductAttribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=32)
    attribute_value = models.TextField()

    def __str__(self):
        return self.attribute


class ProductRelation(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_rel = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_related')

    def __str__(self):
        return self.title
