# Generated by Django 4.1.2 on 2022-11-19 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ven', '0011_alter_nomination_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='sponsor_img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('name', models.TextField(max_length=270)),
            ],
        ),
    ]
