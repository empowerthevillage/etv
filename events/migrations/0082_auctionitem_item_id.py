# Generated by Django 4.1.2 on 2023-08-19 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0081_auctionitem_donor'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionitem',
            name='item_id',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]