from django import forms
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

from .models import dashboardModel
from .signals import user_logged_in

from content.models import contact_submission
from donations.models import donation
from donors.models import Donor
from events.models import Event, SingleTicket, TicketType
from vbp.models import *
from ven.models import Nomination, FamilyNomination

class ContactForm(ModelForm):
    class Meta:
        model = contact_submission
        fields = '__all__'

class DonationForm(ModelForm):
    class Meta:
        model = donation
        fields = '__all__'

class DonorForm(ModelForm):
    class Meta:
        model = Donor
        fields = '__all__'

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

class TicketForm(ModelForm):
    class Meta:
        model = SingleTicket
        fields = '__all__'

class TicketTypeForm(ModelForm):
    class Meta:
        model = TicketType
        fields = '__all__'

class VenBusinessForm(ModelForm):
    class Meta:
        model = Nomination
        fields = '__all__'

class VenFamilyForm(ModelForm):
    class Meta:
        model = FamilyNomination
        fields = '__all__'

class VBPBookForm(ModelForm):
    class Meta:
        model = vbp_book
        fields = '__all__'