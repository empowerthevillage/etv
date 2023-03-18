# Generated by Django 4.1.2 on 2023-02-28 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0011_alter_fullgallerycart_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketad',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carts.ticketcart'),
        ),
        migrations.AlterField(
            model_name='ticketdonation',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carts.ticketcart'),
        ),
    ]