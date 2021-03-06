# Generated by Django 3.2 on 2022-04-09 10:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0041_categoryattribute_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryattribute',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=django.utils.timezone.now, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
