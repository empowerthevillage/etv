from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

STATE_CHOICES = (
    ('', 'State'),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

class DonorForm(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='')
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='')
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'textfield'}), label_suffix='')
    address_line_1 = forms.CharField(label='Mailing Address Line 1', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='', required=False)
    address_line_2 = forms.CharField(label='Mailing Address Line 2', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='', required=False)
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='', required=False)
    state = forms.CharField(label='State', widget=forms.Select(choices=STATE_CHOICES), label_suffix='', required=False)
    zip = forms.CharField(label="Zip Code", widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='', required=False)
    phone = forms.CharField(label='Business Phone', widget=forms.TextInput(attrs={'class':'textfield phone_us'}), label_suffix='', required=False)
    
    def save(self):
            donation = super(DonorForm, self).save()
            return donation