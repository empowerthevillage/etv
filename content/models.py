from django.db import models
from django.conf import settings
import random
import os

User = settings.AUTH_USER_MODEL

class contact_submission(models.Model):
    user             = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    name             = models.CharField(max_length=200)
    email            = models.EmailField()
    message          = models.TextField(blank=True, null=True)
   
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = 'Contact Us Request'
        verbose_name_plural = 'Contact Us Requests'

