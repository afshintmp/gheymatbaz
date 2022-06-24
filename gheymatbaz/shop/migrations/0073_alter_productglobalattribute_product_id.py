# Generated by Django 3.2 on 2022-06-24 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0072_productglobalattribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productglobalattribute',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', unique=True),
        ),
    ]
