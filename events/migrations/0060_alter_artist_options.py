# Generated by Django 3.2.10 on 2022-10-25 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0059_artist_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['pk']},
        ),
    ]
