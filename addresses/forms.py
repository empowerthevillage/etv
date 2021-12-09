from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'name',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'zip_code',
        ]

class ShippingAddressForm(forms.ModelForm):
    type = 'shipping'
    class Meta:
        model = Address
        fields = [
            'name',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'zip_code',
            'billing_profile'
        ]

class BillingAddressForm(forms.ModelForm):
    type = 'billing'
    class Meta:
        model = Address
        fields = [
            'name',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'zip_code',
        ]

class MailingAddressForm(forms.ModelForm):
    type = 'mailing'
    class Meta:
        model = Address
        fields = [
            'name',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'zip_code',
        ]
