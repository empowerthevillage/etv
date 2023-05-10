# Generated by Django 4.1.2 on 2023-04-13 12:28

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('walkathon', '0004_organization_alter_walker_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='walker',
            name='donation_goal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='walker',
            name='emergency_contact_name',
            field=models.CharField(blank=True, max_length=270, null=True),
        ),
        migrations.AddField(
            model_name='walker',
            name='emergency_contact_phone',
            field=phone_field.models.PhoneField(blank=True, max_length=31, null=True),
        ),
        migrations.AddField(
            model_name='walker',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='walkathon.organization'),
        ),
        migrations.DeleteModel(
            name='OrganizationRegistrationPayment',
        ),
    ]