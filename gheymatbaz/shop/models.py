from django.db import models
from django.utils.text import slugify


# Create your models here.

class ProductKeyWord(models.Model):
    keyword = models.CharField(max_length=32, blank=False, null=False)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword


class Brand(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'categories'
        verbose_name_plural = 'categories'


class CategoryAttribute(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, name='category')

    def __str__(self):
        return self.name


class CategoryAttributeValue(models.Model):
    attribute_value = models.CharField(max_length=32, null=False, blank=False)
    parent_attribute_id = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE, name='parent_attribute')

    def __str__(self):
        return self.attribute_value


class Product(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=32, blank=False, null=False)
    slug = models.SlugField(max_length=200, allow_unicode=True, null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='published')

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    view = models.BigIntegerField(default=0)
    rate = models.BigIntegerField(default=0)
    rate_number = models.BigIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('single-product', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    @property
    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return ""


class ProductGallery(models.Model):
    image = models.ImageField(upload_to='product_image', null=False, blank=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    slug = models.SlugField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.product_id

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs)
