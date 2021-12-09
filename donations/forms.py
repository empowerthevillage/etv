from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

DONATION_LEVEL_CHOICES = (
    ('25', 'Village Member - $25'),
    ('50', 'Village Patron - $50'),
    ('100', 'Village Supporter - $100'),
    ('500', 'Village Leader - $500'),
    ('1000', 'Village Ambassador - $1000')
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