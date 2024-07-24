from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from bfchallenge.models import CATEGORY_CHOICES
from etv.utils import unique_subscription_id_generator
from accounts.models import GuestEmail
from addresses.models import Address
from donations.models import donation, donation_event
from events.models import CompleteDonation
from billing.models import Card, BillingProfile
from phone_field import PhoneField
import json

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

    def dashboard_get_fields(self):
        list_fields = [{'field':'total','type':'currency'}, {'field':'first_name','type':'plain'}, {'field':'last_name','type':'plain'},{'field':'phone','type':'phone'},{'field':'email','type':'email'},{'field':'donor_level','type':'plain'}]
        return list_fields
    
    def dashboard_get_view_fields(self):
        fields = [
            {'field':'email','type':'email'},
            {'field':'phone','type':'phone'},
            {'field':'total','type':'currency'},
            {'field':'donor_level','type':'plain'},
            {'field':'company','type':'plain'},
            
            
            {'field':'mailing_addresses','type':'manytomany'},
            {'field':'donations','type':'manytomany'},
        ]
        return fields

    def dashboard_display_qty(self):
        qty = 20
        return qty
        
    def dashboard_category(self):
        category = 'donations'
        return category
    
    def filter_objs(self):
        filtered_qs = Donor.objects.exclude(total=0)
        return filtered_qs

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
    donor_level = models.CharField(max_length=270, null=True, blank=True)
    total       = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    default_mailing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='default_mailing_address', null=True, blank=True)
    mailing_addresses = models.ManyToManyField(Address, blank=True, related_name='mailing_address')
    cards       = models.ManyToManyField(Card, blank=True)
    donations   = models.ManyToManyField(donation, blank=True)
    event_donations = models.ManyToManyField(CompleteDonation, blank=True)
    category    = models.CharField(max_length=270, null=True, blank=True)
    company     = models.CharField(max_length=270, null=True, blank=True)
    events      = models.ManyToManyField(donation_event, blank=True)

    objects = DonorManager()

    def get_full_name(self):
        return "%s %s" %(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()

    def get_cards(self):
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse('billing-payment-method')
    
    class Meta:
        verbose_name = 'Donor'
        verbose_name_plural = 'Donors'
        ordering = ['-total', 'last_name']

    @property
    def get_total(self):
        try:
            donation_list = []
            for x in self.donations.all():
                donation_list.append(x.amount)
            for x in self.event_donations.all():
                donation_list.append(x.amount)
                
            total = sum(donation_list)
            return total
        except:
            pass
    
    @property
    def get_level(self):
        try:
            total = self.total
            if total >= 25000:
                level = "Founder's Circle - Platinum"
            elif total >= 15000:
                level = "Founder's Circle - Gold"
            elif total >= 10000:
                level = "Founder's Circle - Silver"
            elif total >= 5000:
                level = "Founder's Circle - Bronze"
            elif total >= 1000:
                level = "Village Ambassador"
            elif total >= 500:
                level = "Village Leader"
            elif total >= 100:
                level = "Village Supporter"
            elif total >= 50:
                level = "Village Patron"
            elif total >= 25:
                level = "Village Member"
            else:
                level = "Past Donor - Data Unavailable"
            return level
        except:
            pass

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

def donor_total_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.pk is None:
        instance.total = 0
    else:
        instance.total = instance.get_total

def donor_level_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.pk is None:
        instance.donor_level = "Past Donor - Data Unavailable"
    else:
        instance.donor_level = instance.get_level

pre_save.connect(donor_total_pre_save_receiver, sender=Donor)
pre_save.connect(donor_level_pre_save_receiver, sender=Donor)

class List(models.Model):
    donors      = models.ManyToManyField(Donor)
    title       = models.CharField(max_length=270, unique=True)