# Generated by Django 4.0.5 on 2022-06-18 09:28

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_loaartpurchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='loaartpurchase',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='loaartpurchase',
            name='pickup_window',
            field=models.CharField(blank=True, choices=[('11to1', '11am - 1pm'), ('1to3', '1pm - 3pm'), ('3to6', '3pm - 6pm')], max_length=100, null=True),
        ),
    ]