from django.db import models
from bfchallenge.models import everyfriday_transaction
from billing.models import BillingProfile

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
STATE_CHOICES = (
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
DONATION_STATUS_CHOICES = (
    ('incomplete', 'Incomplete'),
    ('complete', 'Complete'),
)
DONATION_FREQUENCY_CHOICES = (
    ('once', 'One Time Donation'),
    ('monthly', 'Monthly Donation')
)

class tag(models.Model):
    tag             = models.CharField(max_length=270, blank=True, null=True)
    def __str__(self):
        return str(self.tag)

class donation_event(models.Model):
    title           = models.CharField(max_length=270, null=True, blank=True)
    total           = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tags            = models.ManyToManyField(tag, blank=True)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

class donation_submission(models.Model):
    first_name      = models.CharField(max_length=50, unique=False)
    last_name       = models.CharField(max_length=50, unique=False)
    email           = models.EmailField(verbose_name='email address', max_length=255, unique=False,)
    donation_level  = models.CharField(max_length=100)
    recurring       = models.CharField(max_length=100, default='once')
    source          = models.CharField(max_length=270, default='Website', null=True, blank=True)
    

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

class DonationManager(models.Manager):

    def new(self, email):
        billing_profile_qs = BillingProfile.objects.get_or_create(
            email=email
        )
        (billing_profile_obj, boolean) = billing_profile_qs
        return self.model.objects.create(billing_profile=billing_profile_obj)

    def add_nonce(self, nonce):
        if nonce:
            return self.update(nonce=nonce)
        return None

class donation(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.SET_NULL)
    first_name      = models.CharField(max_length=50, unique=False)
    last_name       = models.CharField(max_length=50, unique=False)
    amount          = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    frequency       = models.CharField(max_length=100, default='once', choices=DONATION_FREQUENCY_CHOICES)
    status          = models.CharField(max_length=100, choices=DONATION_STATUS_CHOICES, null=True, blank=True)
    braintree_id    = models.CharField(max_length=270, blank=True)
    payment_method  = models.CharField(max_length=270, blank=True)
    subscription_id = models.CharField(max_length=270, null=True, blank=True)
    created         = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated         = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    event           = models.ForeignKey(donation_event, blank=True, null=True, on_delete=models.SET_NULL)
    tags            = models.ManyToManyField(tag, blank=True)

    objects = DonationManager()

    def __str__(self):
        return str(self.id)

