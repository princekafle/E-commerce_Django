# Generated by Django 5.0.6 on 2024-07-09 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_rename_product_name_product_product_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_name',
            new_name='Product_name',
        ),
    ]
