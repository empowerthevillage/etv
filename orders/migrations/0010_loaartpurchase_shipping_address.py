# Generated by Django 3.2.10 on 2022-10-28 19:08

import address.models
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_auto_20200830_1851'),
        ('orders', '0009_alter_loaartpurchase_pickup_window'),
    ]

    operations = [
        migrations.AddField(
            model_name='loaartpurchase',
            name='shipping_address',
            field=address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.address'),
        ),
    ]