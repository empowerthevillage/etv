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

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='')
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'textfield'}), label_suffix='')
    message = forms.CharField(label='Your Message', widget=forms.Textarea(attrs={'class':'materialize-textarea'}), label_suffix='')
    
    def save(self):
        contact_submission = super(ContactForm, self).save()
        return contact_submission