# Generated by Django 4.1.2 on 2023-04-15 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walkathon', '0009_walker_address_line_1_walker_address_line_2_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='walker',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.AddField(
            model_name='walkerdonation',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
