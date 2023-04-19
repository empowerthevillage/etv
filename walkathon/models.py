from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from phone_field import PhoneField
import math

from etv.utils import unique_slug_generator

class Organization(models.Model):
    title                   = models.CharField(max_length=270)
    slug                    = models.SlugField(blank=True, unique=True)
    email                   = models.EmailField(blank=True, null=True)
    bio                     = models.TextField(blank=True)
    image                   = models.ImageField(blank=True, null=True)
    captain_first_name      = models.CharField(max_length=120, null=True, blank=True)
    captain_last_name       = models.CharField(max_length=120, null=True, blank=True)
    donation_goal           = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    
    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("walkathon:walker-detail", kwargs={"walker": self.slug})

    @property
    def goal_truncated(self):
        return math.trunc(self.donation_goal)
    
    @property
    def donation_total(self):
        org_donations = OrgDonation.objects.filter(organization=self)
        total = 0
        individuals = Walker.objects.filter(organization=self)
        for x in individuals:
            donos = WalkerDonation.objects.filter(walker=x)
            for x in donos:
                total += x.amount
        for x in org_donations:
            total += x.amount
        return total
    
    @property
    def donation_total_truncated(self):
        org_donations = OrgDonation.objects.filter(organization=self)
        dono_total = 0
        individuals = Walker.objects.filter(organization=self)
        for x in individuals:
            donos = WalkerDonation.objects.filter(walker=x)
            for x in donos:
                dono_total += x.amount
        for x in org_donations:
            dono_total += x.amount
        return math.trunc(dono_total)
    
    @property
    def get_donations(self):
        donations = OrgDonation.objects.filter(organization=self)
        return donations
        
def org_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(org_pre_save_receiver, sender=Organization)

class Walker(models.Model):
    first_name              = models.CharField(max_length=120)
    last_name               = models.CharField(max_length=120)
    title                   = models.CharField(max_length=270)
    slug                    = models.SlugField(blank=True, unique=True)
    email                   = models.EmailField(blank=True, null=True)
    phone                   = PhoneField(blank=True, null=True)
    bio                     = models.TextField(blank=True)
    image                   = models.ImageField(blank=True, null=True)
    organization            = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    emergency_contact_name  = models.CharField(max_length=270, null=True, blank=True)
    emergency_contact_phone = PhoneField(blank=True, null=True)
    address_line_1          = models.CharField(max_length=270, null=True, blank=True)
    address_line_2          = models.CharField(max_length=270, null=True, blank=True)
    city                    = models.CharField(max_length=120, null=True, blank=True)
    state                   = models.CharField(max_length=120, null=True, blank=True)
    zip                     = models.CharField(max_length=20, null=True, blank=True)
    donation_goal           = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    virtual                 = models.BooleanField(default=False)
    
    def __str__(self):
        return '%s %s' %(self.first_name, self.last_name)

    def get_absolute_url(self):
        if self.organization is not None:
            return reverse("walkathon:group-walker-detail", kwargs={"org": self.organization.slug, "walker": self.slug})
        else:
            return reverse("walkathon:walker-detail", kwargs={"walker": self.slug})
    
    @property
    def goal_truncated(self):
        return math.trunc(self.donation_goal)
    
    @property
    def donation_total(self):
        donations = WalkerDonation.objects.filter(walker=self)
        total = 0
        for x in donations:
            total += x.amount
        return total
    
    @property
    def donation_total_truncated(self):
        donations = WalkerDonation.objects.filter(walker=self)
        total = 0
        for x in donations:
            total += x.amount
        return math.trunc(total)
    
    @property
    def get_donations(self):
        donations = WalkerDonation.objects.filter(walker=self)
        return donations
    
    class Meta:
        ordering = ['last_name', 'first_name']
        
def walker_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(walker_pre_save_receiver, sender=Walker)

class WalkerDonation(models.Model):
    braintree_id            = models.CharField(blank=True, max_length=120)
    complete                = models.BooleanField(default=False)
    message                 = models.TextField(null=True, blank=True)
    first_name              = models.CharField(max_length=120, null=True)
    last_name               = models.CharField(max_length=120, null=True)
    walker                  = models.ForeignKey(Walker, on_delete=models.SET_NULL, null=True)
    address_line_1          = models.CharField(max_length=270, null=True, blank=True)
    address_line_2          = models.CharField(max_length=270, null=True, blank=True)
    city                    = models.CharField(max_length=120, null=True, blank=True)
    state                   = models.CharField(max_length=120, null=True, blank=True)
    zip                     = models.CharField(max_length=20, null=True, blank=True)
    amount                  = models.DecimalField(max_digits=20, decimal_places=2)
    created                 = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '$%s for %s' %(self.amount, self.walker)
    
    class Meta:
        ordering = ['-created']

class OrgDonation(models.Model):
    braintree_id            = models.CharField(blank=True, max_length=120)
    complete                = models.BooleanField(default=False)
    organization            = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    first_name              = models.CharField(max_length=120, null=True)
    last_name               = models.CharField(max_length=120, null=True)
    message                 = models.TextField(null=True, blank=True)
    address_line_1          = models.CharField(max_length=270, null=True, blank=True)
    address_line_2          = models.CharField(max_length=270, null=True, blank=True)
    city                    = models.CharField(max_length=120, null=True, blank=True)
    state                   = models.CharField(max_length=120, null=True, blank=True)
    zip                     = models.CharField(max_length=20, null=True, blank=True)
    amount                  = models.DecimalField(max_digits=20, decimal_places=2)
    created                 = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '$%s for %s' %(self.amount, self.organization)
    
    class Meta:
        ordering = ['-created']

class Sponsorship(models.Model):
    braintree_id            = models.CharField(blank=True, max_length=120)
    complete                = models.BooleanField(default=False)
    first_name              = models.CharField(max_length=120)
    last_name               = models.CharField(max_length=120)
    email                   = models.EmailField(blank=True, null=True)
    phone                   = PhoneField(blank=True, null=True)
    organization            = models.CharField(blank=True, max_length=270, null=True)
    logo                    = models.ImageField(null=True, blank=True)
    message                 = models.TextField(null=True, blank=True)
    amount                  = models.DecimalField(max_digits=20, decimal_places=2)
    created                 = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '$%s for %s' %(self.amount, self.organization)
    
class HomeGalleryImage(models.Model):
    image_id        = models.CharField(max_length=32, blank=True, null=True)
    file            = models.ImageField()
    order           = models.IntegerField(blank=True, null=True)
    caption         = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return str(self.file.url)
    
    class Meta:
        ordering = ['order']
        
class WalkerRegistrationPayment(models.Model):
    braintree_id            = models.CharField(max_length=200, blank=True)
    complete                = models.BooleanField(default=False)
    amount                  = models.DecimalField(max_digits=20, decimal_places=2)
    walker                  = models.ForeignKey(Walker, on_delete=models.SET_NULL, null=True)
    created                 = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s - $%s' %(self.walker, self.amount)

class ShirtOrder(models.Model):
    braintree_id            = models.CharField(max_length=200, blank=True)
    complete                = models.BooleanField(default=False)
    amount                  = models.DecimalField(max_digits=20, decimal_places=2)
    shirt_size              = models.CharField(max_length=270)
    walker                  = models.ForeignKey(Walker, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return 'Size %s for %s' %(self.shirt_size.upper(), self.walker)
