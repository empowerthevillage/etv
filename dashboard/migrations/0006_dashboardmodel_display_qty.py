# Generated by Django 3.2.10 on 2022-04-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_dashboardmodel_list_fields_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardmodel',
            name='display_qty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
