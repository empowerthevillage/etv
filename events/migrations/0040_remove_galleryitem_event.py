# Generated by Django 3.2.10 on 2022-05-04 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0039_galleryitem_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galleryitem',
            name='event',
        ),
    ]