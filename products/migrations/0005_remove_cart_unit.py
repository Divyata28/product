# Generated by Django 2.2.6 on 2019-11-07 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_cart_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='unit',
        ),
    ]
