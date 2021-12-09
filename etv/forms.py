from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.mail import send_mail

User = get_user_model()

from accounts.signals import user_logged_in

class MailchimpForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'textfield'}), label_suffix='')
    
    def save(self):
        mailchimp_subscription = super(MailchimpForm, self).save()
        return mailchimp_subscription