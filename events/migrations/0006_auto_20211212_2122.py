# Generated by Django 3.2.10 on 2021-12-13 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20211208_1930'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='singleticket',
            options={'verbose_name': 'Tickets'},
        ),
        migrations.DeleteModel(
            name='TicketType',
        ),
    ]
