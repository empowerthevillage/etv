# Generated by Django 3.2.10 on 2022-05-19 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_auto_20220518_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='disbursement',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=200),
            preserve_default=False,
        ),
    ]
