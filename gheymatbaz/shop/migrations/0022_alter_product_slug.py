# Generated by Django 3.2 on 2022-03-27 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_productgallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=200, null=True),
        ),
    ]
