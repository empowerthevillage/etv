from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

DONATION_LEVEL_CHOICES = (
    ('1', 'Village Test'),
    ('25', 'Village Member'),
    ('50', 'Village Patron'),
    ('100', 'Village Supporter'),
    ('500', 'Village Leader'),
    ('1000', 'Village Ambassador'),
    ('2500', 'Village Council'),
    ('5000', "Founder's Circle - Bronze"),
    ('10000', "Founder's Circle - Silver"),
    ('15000', "Founder's Circle - Gold"),
    ('25000', "Founder's Circle - Platinum")
)

DONATION_FREQUENCY_CHOICES = (
    ('once', 'One Time Donation'),
    ('monthly', 'Monthly Donation')
)

class DonationForm(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='', required=True)
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='', required=True)
    donor_email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'textfield'}), label_suffix='', required=True)
    donation_level = forms.ChoiceField(label='Donation Amount', widget=forms.RadioSelect(choices=DONATION_LEVEL_CHOICES), label_suffix='', required=True)
    recurring = forms.ChoiceField(label='Please Make My Payment', widget=forms.RadioSelect(choices=DONATION_FREQUENCY_CHOICES), label_suffix='', required=True)