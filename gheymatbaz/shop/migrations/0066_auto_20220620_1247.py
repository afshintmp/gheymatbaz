# Generated by Django 3.2 on 2022-06-20 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0065_auto_20220528_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymeta',
            name='meta_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='categorymeta',
            name='meta_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='categorymeta',
            name='noindex',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
