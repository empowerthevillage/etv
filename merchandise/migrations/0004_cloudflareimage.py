# Generated by Django 4.1.2 on 2023-11-26 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0003_alter_size_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudflareImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=320)),
            ],
        ),
    ]