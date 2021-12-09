from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

from accounts.signals import user_logged_in

CATEGORY_CHOICES = (
    ('beauty','Beauty & Personal Grooming'),
    ('books', 'Books & Publishing'),
    ('cars', 'Cars & Automotive'),
    ('child', "Childcare | Children's Services & Products"),
    ('cleaning', 'Cleaning'),
    ('clothing', 'Clothing & Fashion'),
    ('construction', 'Construction & Trades'),
    ('education', 'Education'),
    ('eldercare', 'Eldercare'),
    ('electronics', 'Electronics & Technology'),
    ('entertainment', 'Entertainment'),
    ('farming', 'Farming & Agriculture'),
    ('florists', 'Florists'),
    ('grocery', 'Grocery & Food Services'),
    ('health', 'Health & Wellness'),
    ('home', 'Home & Garden'),
    ('hotels', 'Hotels & Hospitality | Travel'),
    ('jewelry', 'Jewelry & Accessories'),
    ('legal', 'Legal & Financial Services'),
    ('lifestyle', 'Lifestyle'),
    ('marketing', 'Marketing & Advertising'),
    ('medical', 'Medical Services'),
    ('packaging', 'Packaging | Delivery | Shipping'),
    ('pets', 'Pets & Animal Care'),
    ('photography', 'Photography & Video'),
    ('professional', 'Professional Services'),
    ('real estate', 'Real Estate'),
    ('recreation', 'Recreation & Sports'),
    ('restaurants', 'Restaurants & Bars | Event Spaces'),
    ('security', 'Security Services'),
    ('transportation', 'Transportation & Trucking'),
    ('visual', 'Visual & Performing Arts | Culture'),
    ('other', 'Other'),
)


class RSSForm(forms.Form):
    business_name = forms.CharField(label='Business Name', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='')
    date = forms.DateField(label='Date You Shopped', widget=forms.DateInput(attrs={'class':'datepicker'}), label_suffix='')
    amount = forms.CharField(label='Amount Spent', widget=forms.TextInput(attrs={'class':'textfield money'}), label_suffix='')
    category = forms.CharField(label='Category', widget=forms.Select(choices=CATEGORY_CHOICES), label_suffix='')
    receipt = forms.FileField(label='Receipt', widget=forms.ClearableFileInput(attrs={'class':'file-path validate','placeholder':'Upload a Photo/Screenshot of Your Receipt', 'type':'text', 'name':'receipt'}), label_suffix='', required=False)
    
    def save(self):
            rss_transaction = super(RSSForm, self).save()
            return rss_transaction

class EFForm(forms.Form):
    business_name = forms.CharField(label='Business Name', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='')
    date = forms.DateField(label='Date You Shopped', widget=forms.DateInput(attrs={'class':'datepicker'}), label_suffix='')
    amount = forms.CharField(label='Amount Spent', widget=forms.TextInput(attrs={'class':'textfield money'}), label_suffix='')
    category = forms.CharField(label='Category', widget=forms.Select(choices=CATEGORY_CHOICES), label_suffix='')
    receipt = forms.FileField(label='Receipt', widget=forms.ClearableFileInput(attrs={'class':'file-path validate','placeholder':'Upload a Photo/Screenshot of Your Receipt', 'type':'text', 'required':'False'}), label_suffix='')
    
    def save(self):
            rss_transaction = super(RSSForm, self).save()
            return rss_transaction
class STLForm(forms.Form):
    link = forms.CharField(label='Instagram Post Link', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='')