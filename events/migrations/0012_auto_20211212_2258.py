# Generated by Django 3.2.10 on 2021-12-13 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_tickettype_sponsorship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickettype',
            name='add_ons',
        ),
        migrations.AddField(
            model_name='singleticket',
            name='add_ons',
            field=models.ManyToManyField(blank=True, to='events.AddOn'),
        ),
    ]
