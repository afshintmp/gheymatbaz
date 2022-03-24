from django.db import models


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
    title = models.CharField(max_length=32, blank=False, null=False)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    view = models.BigIntegerField(default=0)
    rate = models.BigIntegerField(default=0)
    rate_number = models.BigIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
