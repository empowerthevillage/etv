# Generated by Django 3.2.10 on 2022-04-06 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardmodel',
            name='model_name_plural',
            field=models.CharField(default='Donations', max_length=200),
            preserve_default=False,
        ),
    ]
