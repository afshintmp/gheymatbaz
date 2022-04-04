# Generated by Django 3.2 on 2022-04-04 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_alter_brand_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='shop.Category'),
        ),
    ]
