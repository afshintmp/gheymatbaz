# Generated by Django 3.2 on 2022-06-24 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0071_auto_20220624_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGlobalAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('global_attribute', models.ManyToManyField(to='shop.GlobalAttribute')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]
