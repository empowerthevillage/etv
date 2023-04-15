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
    
    def __str__(self):
        return '%s %s' %(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse("walkathon:walker-detail", kwargs={"walker": self.slug})
    
    @property
    def goal_truncated(self):
        return math.trunc(self.donation_goal)
    
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
    walker                  = models.ForeignKey(Walker, on_delete=models.SET_NULL, null=True)
    amount                  = models.DecimalField(max_digits=20, decimal_places=2)
    created                 = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '$%s for %s' %(self.amount, self.walker)

class OrgDonation(models.Model):
    braintree_id            = models.CharField(blank=True, max_length=120)
    complete                = models.BooleanField(default=False)
    organization            = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
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
        return str(self.walker)

class ShirtOrder(models.Model):
    braintree_id            = models.CharField(max_length=200, blank=True)
    complete                = models.BooleanField(default=False)
    amount                  = models.DecimalField(max_digits=20, decimal_places=2)
    shirt_size              = models.CharField(max_length=270)
    walker                  = models.ForeignKey(Walker, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return 'Size %s for %s' %(self.shirt_size, self.walker)
