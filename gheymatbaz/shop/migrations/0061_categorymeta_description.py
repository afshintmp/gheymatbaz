# Generated by Django 3.2 on 2022-05-22 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0060_categorymeta'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymeta',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
