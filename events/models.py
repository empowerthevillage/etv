from datetime import date
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.http import HttpResponse
from django.urls import reverse
from itertools import islice
from etv.utils import unique_ticket_id_generator, unique_slug_generator
from billing.models import BillingProfile
from tinymce.models import HTMLField

from ckeditor.fields import RichTextField
from django_quill.fields import QuillField

class tag(models.Model):
    tag             = models.CharField(max_length=270, blank=True, null=True)
    def __str__(self):
        return str(self.tag)

class Event(models.Model):
    title           = models.CharField(max_length=270)
    content         = HTMLField()
    slug            = models.SlugField()
    details         = QuillField()
    date            = models.DateTimeField(blank=True, null=True)
    tags            = models.ManyToManyField(tag, blank=True)
    thumbnail       = models.FileField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"slug":self.slug})
    
    def __str__(self):
        return str(self.title)

def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(event_pre_save_receiver, sender=Event)

class Option(models.Model):
    title = models.CharField(max_length=270)

    def __str__(self):
        return self.title

class AddOn(models.Model):
    title           = models.CharField(max_length=270, null=True, blank=True)
    description     = models.TextField(blank=True)
    price           = models.DecimalField(decimal_places=2, max_digits=10)
    options         = models.ManyToManyField(Option, blank=True)

    def __str__(self):
        return self.title

class Guest(models.Model):
    first_name      = models.CharField(max_length=270, null=True, blank=True)
    last_name       = models.CharField(max_length=270, null=True, blank=True)
    email           = models.EmailField()

    def __str__(self):
        return '%s %s' %(self.first_name, self.last_name)

class TicketType(models.Model):
    title           = models.CharField(max_length=270, null=True, blank=True)
    sponsorship     = models.BooleanField(default=False)
    price           = models.DecimalField(decimal_places=2, max_digits=10)
    quantity        = models.IntegerField(null=True, blank=True)
    event           = models.ForeignKey(Event, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title

    @property
    def is_sponsorship(self):
        return self.sponsorship

    class Meta:
        verbose_name = 'Ticket Type'
        verbose_name_plural = 'Ticket Types'

class TicketManagerQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created =BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')

class TicketManager(models.Manager):
    def get_queryset(self):
        return TicketManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False

        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status='created').first()
        if qs != None:
            obj = qs
            print(obj)
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj)
            created = True
        return obj, created

class SingleTicket(models.Model):
    title           = models.CharField(max_length=270, null=True, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.SET_NULL, null=True, blank=True)
    type            = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True, blank=True)
    ticket_id       = models.CharField(max_length=270, blank=True)
    event           = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    guest           = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True)
    email           = models.EmailField(blank=True, null=True)
    group           = models.CharField(max_length=270, null=True, blank=True)
    add_ons         = models.ManyToManyField(AddOn, blank=True)
    qr_code         = models.ImageField(null=True, blank=True)
    guest_list      = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.ticket_id

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def get_absolute_url(self):
        return reverse("events:ticket-detail", kwargs={"ticket_id":self.ticket_id} )

    def get_qr_code_path(self):
            return 'https://d1z669787inm16.cloudfront.net/media/%s' %(self.qr_code)
            
def ticket_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.ticket_id:
        instance.ticket_id = unique_ticket_id_generator(instance)

pre_save.connect(ticket_pre_save_receiver, sender=SingleTicket)
