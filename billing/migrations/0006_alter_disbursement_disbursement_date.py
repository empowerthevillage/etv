# Generated by Django 3.2.10 on 2022-05-19 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_disbursement_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disbursement',
            name='disbursement_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]