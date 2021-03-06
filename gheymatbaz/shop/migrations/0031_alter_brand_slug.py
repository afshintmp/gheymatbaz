# Generated by Django 3.2 on 2022-04-03 10:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_auto_20220403_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=django.utils.timezone.now, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
