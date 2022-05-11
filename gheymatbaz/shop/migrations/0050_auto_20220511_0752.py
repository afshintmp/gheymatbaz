# Generated by Django 3.2 on 2022-05-11 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0049_product_noindex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category_attribute_value',
        ),
        migrations.CreateModel(
            name='ProductCategoryAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_header', models.BooleanField()),
                ('category_attribute_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.categoryattributevalue')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]