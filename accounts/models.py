from datetime import timedelta
import random
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from django.db import models
from django.db import IntegrityError
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.core.mail import send_mail
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

mailchimp = Client()
mailchimp.set_config({
    "api_key": settings.MAILCHIMP_API_KEY,
    "server": "us7"
})

CHALLENGE_CHOICES = (
    ('bingo', 'Power Bingo'),
    ('rss', 'Ready, Set, Shop!')
)
class MyUserManager(BaseUserManager):
    def create_user(self, email, username=None, is_active=True, staff=False, admin=False, password=None):
        if not email:
            raise ValueError('An email address is required')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.staff = staff
        user.is_active = user.active
        user.admin = admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, password, email):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, password, email):
        user = self.create_user(
            email,
            password=password,
            username=username
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=225, blank=True, null=True, unique=False)
    first_name = models.CharField(max_length=225, blank=True, null=True, unique=False)
    last_name = models.CharField(max_length=225, blank=True, null=True, unique=False)
    active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)
    is_donor = models.BooleanField(default=False, blank=True, null=True)
    rss_sponsor = models.BooleanField(default=False, blank=True, null=True)
    bingo_sponsor = models.BooleanField(default=False, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_donor(self):
        return self.is_donor

    @property
    def is_rss_sponsor(self):
        return self.rss_sponsor
    
    @property
    def is_bingo_sponsor(self):
        return self.bingo_sponsor

class GuestEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class Team(models.Model):
    team_name = models.CharField(max_length=200, unique=True)
    paid = models.BooleanField(default=False)
    challenge_access = models.CharField(choices=CHALLENGE_CHOICES, blank=True, max_length=100)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.team_name

class Participant(models.Model):
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.email