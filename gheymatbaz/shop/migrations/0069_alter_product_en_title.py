# Generated by Django 3.2 on 2022-06-22 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0068_product_en_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='en_title',
            field=models.CharField(blank=True, default='', max_length=400, null=True),
        ),
    ]
