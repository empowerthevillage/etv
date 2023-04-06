from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from etv.utils import unique_slug_generator

class Walker(models.Model):
    first_name              = models.CharField(max_length=120)
    last_name               = models.CharField(max_length=120)
    title                   = models.CharField(max_length=270)
    slug                    = models.SlugField(blank=True)
    email                   = models.EmailField(blank=True, null=True)
    bio                     = models.TextField(blank=True)
    image                   = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return '%s %s' %(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse("walkathon:walker-detail", kwargs={"walker": self.slug})
    
def walker_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(walker_pre_save_receiver, sender=Walker)

class WalkerDonation(models.Model):
    braintree_id            = models.CharField(blank=True, max_length=120)
    complete                = models.BooleanField(default=False)
    walker                  = models.ForeignKey(Walker, on_delete=models.SET_NULL, null=True)
    amount                  = models.DecimalField(max_digits=20, decimal_places=2)
    created                 = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '$%s for %s' %(self.amount, self.walker)
    
class HomeGalleryImage(models.Model):
    image_id        = models.CharField(max_length=32, blank=True, null=True)
    file            = models.ImageField()
    order           = models.IntegerField(blank=True, null=True)
    caption         = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return str(self.file.url)
    
    class Meta:
        ordering = ['order']