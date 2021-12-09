from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from bfchallenge.models import CATEGORY_CHOICES
from etv.utils import unique_subscription_id_generator
from accounts.models import GuestEmail
from addresses.models import Address
from donations.models import donation, donation_event
from billing.models import Card, BillingProfile
from phone_field import PhoneField

import braintree

User = settings.AUTH_USER_MODEL
gateway = settings.GATEWAY

DONATION_LEVEL_CHOICES = (
    ('25', 'Village Member'),
    ('50', 'Village Patron'),
    ('100', 'Village Supporter'),
    ('500', 'Village Leader'),
    ('1000', 'Village Ambassador'),
    ('5000', "Founder's Circle - Bronze"),
    ('10000', "Founder's Circle - Silver"),
    ('15000', "Founder's Circle - Gold"),
    ('25000', "Founder's Circle - Platinum"),
)

class DonorManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email = request.session.get('guest_email')
        created = False
        obj = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(
            user=user,
            email=user.email)
        elif guest_email is not None:
            guest_email_obj = GuestEmail.objects.get(email=guest_email)
            obj, created = self.model.objects.get_or_create(
            email=guest_email_obj.email)
        else:
            pass
        return obj, created

class Donor(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.CharField(max_length=270, null=True, blank=True)
    email       = models.EmailField(null=True, blank=True)
    active      = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True, null=True, blank=True)
    created     = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    donor_id    = models.CharField(max_length=120, null=True, blank=True)
    first_name  = models.CharField(max_length=120, null=True, blank=True)
    last_name   = models.CharField(max_length=120, null=True, blank=True)
    phone       = PhoneField(blank=True, null=True)
    donor_level = models.CharField(choices=DONATION_LEVEL_CHOICES, max_length=270, null=True, blank=True)
    default_mailing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='default_mailing_address', null=True, blank=True)
    mailing_addresses = models.ManyToManyField(Address, blank=True, related_name='mailing_address')
    cards       = models.ManyToManyField(Card, blank=True)
    donations   = models.ManyToManyField(donation, blank=True)
    category    = models.CharField(max_length=270, null=True, blank=True)
    company     = models.CharField(max_length=270, null=True, blank=True)
    events      = models.ManyToManyField(donation_event, blank=True)

    objects = DonorManager()

    def __str__(self):
        return str(self.id)

    def get_cards(self):
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse('billing-payment-method')

    @property
    def has_card(self):
        instance = self
        card_qs = instance.get_cards()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()

class List(models.Model):
    donors      = models.ManyToManyField(Donor)
    title       = models.CharField(max_length=270, unique=True)