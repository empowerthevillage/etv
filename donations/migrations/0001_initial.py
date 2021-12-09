# Generated by Django 3.2.8 on 2021-10-31 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='donation_submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255, verbose_name='email address')),
                ('donation_level', models.CharField(max_length=100)),
                ('recurring', models.CharField(default='once', max_length=100)),
            ],
            options={
                'verbose_name': 'Donation',
                'verbose_name_plural': 'Donations',
            },
        ),
        migrations.CreateModel(
            name='donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('frequency', models.CharField(choices=[('once', 'One Time Donation'), ('monthly', 'Monthly Donation')], default='once', max_length=100)),
                ('status', models.CharField(blank=True, choices=[('incomplete', 'Incomplete'), ('complete', 'Complete')], max_length=100, null=True)),
                ('braintree_id', models.CharField(blank=True, max_length=270)),
                ('payment_method', models.CharField(blank=True, max_length=270)),
                ('subscription_id', models.CharField(blank=True, max_length=270, null=True)),
                ('created', models.DateTimeField(auto_now=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('billing_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='billing.billingprofile')),
            ],
        ),
    ]
