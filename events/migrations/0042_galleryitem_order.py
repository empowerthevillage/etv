# Generated by Django 3.2.10 on 2022-05-04 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0041_galleryitem_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryitem',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
