import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.db.models.fields import SlugField
from django.conf import settings
from accounts.models import Team
from phone_field import PhoneField

import geocoder
import django_filters

User = settings.AUTH_USER_MODEL

STATE_CHOICES = [
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
]
CATEGORY_CHOICES = [
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
]

class vbpusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approved=True)

class vbpus(models.Model):
    directory_source            = models.CharField(max_length=200, null=True, blank=True)
    business_name               = models.CharField(max_length=200)
    website                     = models.URLField(blank=True, max_length=500, null=True)
    instagram                   = models.URLField(blank=True, null=True, max_length=200)
    twitter                     = models.URLField(blank=True, null=True, max_length=200)
    facebook                    = models.URLField(blank=True, null=True, max_length=200)
    city                        = models.CharField(max_length=100, null=True, blank=True)
    county                      = models.CharField(max_length=200, blank=True, null=True)
    state                       = models.CharField(max_length=50, choices=STATE_CHOICES, null=True, blank=True)
    phone                       = PhoneField(blank=True, null=True, help_text='Business Phone Number')
    category                    = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True)
    subcategory                 = models.CharField(max_length=200, blank=True, null=True)
    online_only                 = models.BooleanField(default=False)
    nominator_name              = models.CharField(max_length=300, blank=True, null=True)
    nominator_email             = models.EmailField(blank=True, null=True)
    nominator_owner             = models.BooleanField(default=False, blank=True, null=True)
    nominator_recommended       = models.BooleanField(default=False, blank=True, null=True)    
    owner_name                  = models.CharField(max_length=300, blank=True, null=True)
    owner_email                 = models.EmailField(blank=True, null=True)
    approved                    = models.BooleanField(default=False, null=True)
    created                     = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated                     = models.DateTimeField(auto_now=True, blank=True, null=True)
    user                        = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)

    objects = vbpusManager()

    def __str__(self):
        return str(self.business_name)

    @property
    def is_approved(self):
         return self.approved

    class Meta:
        verbose_name = 'VBP Listing'
        verbose_name_plural = 'VBP Listings'

class vbpus_book(models.Model):
    state           = models.CharField(max_length=50, choices=STATE_CHOICES)
    cover           = models.ImageField(null=True, blank=True)
    published       = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.state)
    
    @property
    def is_published(self):
        return self.is_published

    class Meta:
        verbose_name = 'VBP Cover'
        verbose_name_plural = 'VBP Covers'