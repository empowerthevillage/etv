# Generated by Django 4.1.2 on 2023-07-21 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0074_galleryitem_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='fullgalleryitem',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]