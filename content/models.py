from django.db import models
from django.conf import settings
from tinymce.models import HTMLField

import random
import os
import json

User = settings.AUTH_USER_MODEL

class contactManager(models.Manager):
    def filter_objs(self):
        filtered_qs = self
        return filtered_qs
        
    def dashboard_get_fields(self):
        list_fields = [{'field':'name','type':'plain'},{'field':'email','type':'message'},]
        return json.dumps(list_fields)
    
    def dashboard_get_view_fields(self):
        fields = [
            {'field':'user','type':'plain'},
            {'field':'name','type':'plain'}, 
            {'field':'email','type':'email'},
            {'field':'message','type':'plain'},
        ]
        return json.dumps(fields)
    
    def dashboard_display_qty(self):
        qty = 30
        return qty
        
    def dashboard_category(self):
        category = 'Contact Us'
        return category

class contact_submission(models.Model):
    user             = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    name             = models.CharField(max_length=200)
    email            = models.EmailField()
    message          = models.TextField(blank=True, null=True)
    received         = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    objects          = contactManager()
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = 'Contact Us Request'
        verbose_name_plural = 'Contact Us Requests'

class news_content(models.Model):
    content          = HTMLField()

    class Meta:
        verbose_name = 'News Page Content'
        verbose_name_plural = 'News Page Content'