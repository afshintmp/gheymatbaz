# Generated by Django 3.2 on 2022-03-23 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_category_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryattribute',
            old_name='category_id',
            new_name='category',
        ),
    ]
