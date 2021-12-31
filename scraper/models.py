from django.contrib.admin.options import csrf_protect_m
from django.db import models
from phone_field import PhoneField

class VBPScraped(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=400, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    subcategory = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=270, blank=True, null=True)
    county = models.CharField(max_length=270, blank=True, null=True)
    zip = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'