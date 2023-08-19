
from datetime import date
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.http import HttpResponse
from django.urls import reverse
from itertools import islice
from etv.utils import *
from billing.models import BillingProfile
from tinymce.models import HTMLField
import qrcode
import json
from PIL import Image, ImageDraw
import qrcode.image.svg
import django_filters
from io import BytesIO
from django.core.files import File

from ckeditor.fields import RichTextField

class tag(models.Model):
    tag             = models.CharField(max_length=270, blank=True, null=True)
    def __str__(self):
        return str(self.tag)

class EventManager(models.Manager):
    def filter_objs(self):
        filtered_qs = self
        return filtered_qs
        
    def dashboard_get_fields(self):
        list_fields = [{'field':'title','type':'plain'},{'field':'start_date','type':'datetime'},{"field":'start_time','type':'datetime'}]
        return list_fields
    
    def dashboard_get_view_fields(self):
        fields = [
            {'field':'title','type':'plain'},
            {'field':'subtitle','type':'plain'},
            {'field':'thumbnail','type':'img'},  
            {'field':'content','type':'richtext'},
            {'field':'checkout_image','type':'img'},
            {'field':'checkout_img_link','type':'url'},
            {'field':'checkout_video_html','type':'html'},
            {'field':'date','type':'datetime'},
            {'field':'start_date','type':'date'},
            {'field':'end_date','type':'date'},
            {'field':'start_time','type':'time'},
            {'field':'end_time','type':'time'},
        ]
        return json.dumps(fields)
    
    def dashboard_display_qty(self):
        qty = 10
        return qty
        
    def dashboard_category(self):
        category = 'Events'
        return category

class PhotoGalleryItem(models.Model):
    image = models.ImageField()
    
    
class Event(models.Model):
    title           = models.CharField(max_length=270)
    subtitle        = models.CharField(max_length=270, null=True, blank=True)
    content         = HTMLField(null=True, blank=True)
    page_content    = RichTextField(null=True, blank=True)
    slug            = models.SlugField()
    checkout_image  = models.ImageField(blank=True, null=True)
    checkout_img_url = models.URLField(blank=True, null=True)
    checkout_img_link = models.CharField(max_length=270, null=True, blank=True)
    checkout_image_2  = models.ImageField(blank=True, null=True)
    checkout_img_link_2 = models.CharField(max_length=270, null=True, blank=True)
    date            = models.DateTimeField(blank=True, null=True)
    start_date      = models.DateField(blank=True, null=True)
    end_date        = models.DateField(blank=True, null=True)
    start_time      = models.TimeField(blank=True, null=True)
    end_time        = models.TimeField(blank=True, null=True)
    tags            = models.ManyToManyField(tag, blank=True)
    thumbnail       = models.FileField(null=True, blank=True)
    price_description = models.CharField(max_length=270, null=True, blank=True)
    checkout_video_html = HTMLField(null=True, blank=True)
    has_gallery     = models.BooleanField(default=False, null=True, blank=True)
    gallery_photos = models.ManyToManyField(PhotoGalleryItem, blank=True)
    sponsor_image   = models.ImageField(blank=True, null=True)
    objects         = EventManager()

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"slug":self.slug})
    
    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['title']

    @property
    def is_multiday(self):
        if self.end_date > self.start_date:
            return True
        else:
            return False

    @property
    def get_checkout_img_path(self):
        return str(self.checkout_img_url)
    
    @property
    def get_checkout_img_path_2(self):
        return 'https://d1z669787inm16.cloudfront.net/media/%s' %(self.checkout_image_2)
    
    @property
    def get_sponsor_img_path(self):
        return 'https://d1z669787inm16.cloudfront.net/media/%s' %(self.sponsor_image)

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

class TicketTypeManager(models.Manager):
    def filter_objs(self):
        filtered_qs = self
        return filtered_qs
        
    def dashboard_get_fields(self):
        list_fields = [{'field':'event','type':'plain'},{'field':'title','type':'plain'},{'field':'price','type':'currency'}]
        return list_fields
    
    def dashboard_get_view_fields(self):
        fields = [
            {'field':'event','type':'plain'},
            {'field':'title','type':'plain'},
            {'field':'description','type':'plain'},
            {'field':'price','type':'currency'},
            {'field':'sale','type':'boolean'},
            {'field':'sale_price','type':'currency'},
            {'field':'sale_description','type':'plain'},
            {'field':'sponsorship','type':'boolean'},
            {'field':'quantity','type':'plain'},
        ]
        return fields
    
    def dashboard_display_qty(self):
        qty = 40
        return qty
        
    def dashboard_category(self):
        category = 'Events'
        return category

class TicketType(models.Model):
    title           = models.CharField(max_length=270, null=True, blank=True)
    sponsorship     = models.BooleanField(default=False)
    price           = models.DecimalField(decimal_places=2, max_digits=10)
    sale            = models.BooleanField(default=False)
    sale_price      = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    sale_description = models.CharField(max_length=270, null=True, blank=True)
    quantity        = models.IntegerField(null=True, blank=True)
    event           = models.ForeignKey(Event, on_delete=models.CASCADE)
    description     = models.TextField(null=True, blank=True)
    price_description = models.CharField(max_length=270, null=True, blank=True)
    order           = models.IntegerField(null=True, blank=True)
    active          = models.BooleanField(default=True)
    registration_url = models.CharField(max_length=370, blank=True, null=True)
    registration_text = models.TextField(blank=True, null=True)
    
    objects         = TicketTypeManager()

    def __str__(self):
        return str(self.title)

    @property
    def on_sale(self):
        return self.sale

    @property
    def get_price(self):
        if self.sale == True:
            return self.sale_price
        else:
            return self.price

    @property
    def is_sponsorship(self):
        return self.sponsorship

    class Meta:
        verbose_name = 'Ticket Type'
        verbose_name_plural = 'Ticket Types'
        ordering = ['event', 'order', 'price']

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
    def filter_objs(self):
        filtered_qs = self
        return filtered_qs
        
    def dashboard_get_fields(self):
        list_fields = [{'field':'event','type':'plain'},{'field':'type','type':'plain'},{'field':'purchase_price','type':'currency'},{"field":'first_name','type':'plain'},{"field":'last_name','type':'plain'}]
        return list_fields
    
    def dashboard_get_view_fields(self):
        fields = [
            {'field':'event','type':'foreignkey'},
            {'field':'type','type':'foreignkey'},
            {'field':'ticket_id','type':'plain'},
            {'field':'braintree_id', 'type':'braintree_transaction'},
            {'field':'purchase_price','type':'currency'},
            {'field':'first_name','type':'plain'},
            {'field':'last_name','type':'plain'},
            {'field':'email','type':'email'},
            {'field':'guest_list','type':'plain'},
            {'field':'qr_code','type':'img'},
            {'field':'created','type':'datetime'},
        ]
        return fields
    
    def dashboard_display_qty(self):
        qty = 20
        return qty
        
    def dashboard_category(self):
        category = 'orders'
        return category

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
    first_name      = models.CharField(max_length=100, null=True, blank=True)
    last_name       = models.CharField(max_length=100, null=True, blank=True)
    created         = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated         = models.DateTimeField(auto_now=True, null=True, blank=True)
    purchase_price  = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    braintree_id    = models.CharField(max_length=270, blank=True, null=True)
    checked_in      = models.BooleanField(default=False, blank=True, null=True)

    objects         = TicketManager()
    def __str__(self):
        return self.ticket_id

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse("events:ticket-detail", kwargs={"ticket_id":self.ticket_id} )

    def get_qr_code_path(self):
            return 'https://d1z669787inm16.cloudfront.net/media/%s' %(self.qr_code)

    def get_full_name(self):
        return "%s %s" %(self.first_name, self.last_name) 
        
def ticket_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.ticket_id:
        instance.ticket_id = unique_ticket_id_generator(instance)
    if not instance.qr_code:
        url = "https://www.empowerthevillage.org/events/ticket/%s" %(instance.ticket_id)
        code = qrcode.make(str(url))
        canvas = Image.new("RGB", (415,415), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(code)
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        instance.qr_code.save("qr-code-%s.png" %(instance.ticket_id),File(buffer),save=False)
        canvas.close()

pre_save.connect(ticket_pre_save_receiver, sender=SingleTicket)


class AdType(models.Model):
    title               = models.CharField(max_length=270, null=True, blank=True)
    event               = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    price               = models.DecimalField(decimal_places=2, max_digits=10)
    sale                = models.BooleanField(default=False)
    sale_price          = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    sale_description    = models.CharField(max_length=270, null=True, blank=True)
    description         = HTMLField(null=True, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ad Type'
        verbose_name_plural = 'Ad Types'
        ordering = ['price']

class AdManager(models.Manager):

    def filter_objs(self):
        filtered_qs = self
        return filtered_qs
        
    def dashboard_get_fields(self):
        list_fields = [{'field':'type','type':'plain'},{'field':'event','type':'plain'},{'field':'email','type':'email'},{"field":'first_name','type':'plain'},{"field":'last_name','type':'plain'}]
        return list_fields
    
    def dashboard_get_view_fields(self):
        fields = [
            {'field':'ad','type':'image'},
            {'field':'ad_id','type':'plain'},
            {'field':'type','type':'foreignkey'},
            {'field':'event','type':'foreignkey'},
            {'field':'email','type':'email'},
            {"field":'first_name','type':'plain'},
            {"field":'last_name','type':'plain'}
            ]
        return fields
    
    def dashboard_display_qty(self):
        qty = 15
        return qty
        
    def dashboard_category(self):
        category = 'Events'
        return category

class Ad(models.Model):
    ad              = models.ImageField(null=True, blank=True)
    type            = models.ForeignKey(AdType, on_delete=models.SET_NULL, null=True, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.SET_NULL, null=True, blank=True)
    ad_id           = models.CharField(max_length=270, blank=True)
    event           = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    email           = models.EmailField(blank=True, null=True)
    first_name      = models.CharField(max_length=100, null=True, blank=True)
    last_name       = models.CharField(max_length=100, null=True, blank=True)
    braintree_id    = models.CharField(max_length=270, blank=True)
    
    objects         = AdManager()

    def __str__(self):
        return self.ad_id

    class Meta:
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'

def ad_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.ad_id:
        instance.ad_id = unique_ad_id_generator(instance)

pre_save.connect(ad_pre_save_receiver, sender=Ad)

class EventDonationManager(models.Manager):

    def filter_objs(self):
        filtered_qs = self
        return filtered_qs
        
    def dashboard_get_fields(self):
        list_fields = [
            {'field':'event','type':'plain'},
            {'field':'amount','type':'currency'},
            {'field':'first_name','type':'plain'},
            {'field':'last_name','type':'plain'},
            {'field':'email','type':'email'},
            ]
        return list_fields
    
    def dashboard_get_view_fields(self):
        fields = [
            {'field':'event','type':'foreignkey'},
            {'field':'amount','type':'currency'},
            {'field':'first_name','type':'plain'},
            {'field':'last_name','type':'plain'},
            {'field':'email','type':'email'},
            {'field':'braintree_id','type':'braintree_transaction'},
            {'field':'created','type':'datetime'},
            ]
        return fields
    
    def dashboard_display_qty(self):
        qty = 20
        return qty
        
    def dashboard_category(self):
        category = 'donations'
        return category

class CompleteDonation(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.SET_NULL, null=True, blank=True)
    event           = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    email           = models.EmailField(blank=True, null=True)
    first_name      = models.CharField(max_length=100, null=True, blank=True)
    last_name       = models.CharField(max_length=100, null=True, blank=True)
    amount          = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    braintree_id    = models.CharField(max_length=270, blank=True)
    created         = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated         = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    objects         = EventDonationManager()

    def __str__(self):
        return '$%s Event Donation from %s %s' %(self.amount, self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Event Donation'
        verbose_name_plural = 'Event Donations'
        ordering = ['-created']

class Artist(models.Model):
    name            = models.CharField(max_length=270)
    image           = models.FileField(blank=True, null=True)
    image_url       = models.URLField(blank=True, null=True)
    bio             = models.TextField(null=True, blank=True)
    active          = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['pk']

class GalleryManager(models.Manager):

    def filter_objs(self):
        filtered_qs = self
        return filtered_qs
        
    def dashboard_get_fields(self):
        list_fields = [{'field':'title','type':'plain'},{'field':'artist','type':'foreignkey'},{"field":'price','type':'currency'},{'field':'sold','type':'boolean'}]
        return list_fields
    
    def dashboard_get_view_fields(self):
        fields = [{'field':'title','type':'plain'},{'field':'artist','type':'foreignkey'},{"field":'description','type':'plain'},{"field":'price','type':'currency'},{'field':'image','type':'image'},{'field':'width','type':'plain'},{'field':'height','type':'plain'},{'field':'sold','type':'boolean'},{'field':'order','type':'plain'}]
        return fields
    
    def dashboard_display_qty(self):
        qty = 20
        return qty
        
    def dashboard_category(self):
        category = 'Events'
        return category

class GalleryItem(models.Model):
    
    title           = models.CharField(max_length=270)
    artist          = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True)
    image           = models.ImageField(blank=True)
    image_url       = models.URLField(blank=True, null=True)
    description     = models.TextField(blank=True)
    price           = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    width           = models.CharField(max_length=20, blank=True)
    height          = models.CharField(max_length=20, blank=True)
    sold            = models.BooleanField(default=False)
    order           = models.IntegerField(null=True, blank=True)
    pre_sale        = models.BooleanField(default=False)
    donated         = models.BooleanField(default=False)
    note            = models.CharField(max_length=270, null=True, blank=True)

    objects         = GalleryManager()
    
    class Meta:
        verbose_name = 'Juneteenth Pre-Sale Art Show Item'
        verbose_name_plural = 'Juneteenth Pre-Sale Art Show Items'
        ordering = ['artist', 'price']

    def __str__(self):
        return str(self.title)

    @property
    def get_availability(self):
        return self.sold
    
class FullGalleryItem(models.Model):
    
    title           = models.CharField(max_length=270)
    artist          = models.CharField(max_length=270)
    image           = models.ImageField(blank=True)
    image_url       = models.URLField(blank=True, null=True)
    description     = models.TextField(blank=True)
    price           = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    width           = models.CharField(max_length=20, blank=True)
    height          = models.CharField(max_length=20, blank=True)
    sold            = models.BooleanField(default=False)
    order           = models.IntegerField(null=True, blank=True)
    pre_sale        = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)
    year            = models.BigIntegerField(default=2022)
    donated         = models.BooleanField(default=False)
    note            = models.CharField(max_length=270, null=True, blank=True)

    objects         = GalleryManager()
    
    class Meta:
        verbose_name = 'Juneteenth Art Show Item'
        verbose_name_plural = 'Juneteenth Art Show Items'
        ordering = ['-sold', 'artist', 'title']

    def __str__(self):
        return str(self.title)

    @property
    def get_availability(self):
        return self.sold

class AuctionItem(models.Model):
    event           = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    item_id         = models.CharField(max_length=32, null=True, blank=True)
    title           = models.CharField(max_length=270)
    donor           = models.CharField(max_length=270, null=True, blank=True)
    image_link      = models.URLField(blank=True, null=True)
    description     = models.TextField(blank=True)
    active          = models.BooleanField(default=True)
    sold            = models.BooleanField(default=False)
    buy_now_price   = models.DecimalField(decimal_places=2, max_digits=30, default=0.00)
    minimum_bid     = models.DecimalField(decimal_places=2, max_digits=30, default=0.00)
    order           = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.title)
    
    def get_buy_now_url(self):
        return str('/events/2023-power-swing-silent-auction/buy-now/%s' %(self.item_id))
    
    class Meta:
        ordering = ['order']
    
class GalleryFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    artist = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = FullGalleryItem
        fields = ['artist', 'title']

class TicketFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = SingleTicket
        fields = ['last_name', 'first_name', 'ticket_id', 'email']
        
class CheckIn(models.Model):
    tickets         = models.ManyToManyField(SingleTicket, blank=True)
    email           = models.EmailField(null=True, blank=True)
    first_name      = models.CharField(max_length=270, null=True, blank=True)
    last_name       = models.CharField(max_length=270, null=True, blank=True)
    guests          = models.IntegerField(default=0, null=True, blank=True)
    guest_list      = models.TextField(null=True, blank=True)
    time            = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-time']
        
class Signature(models.Model):
    purpose         = models.CharField(max_length=270)
    first_name      = models.CharField(max_length=270, null=True, blank=True)
    last_name       = models.CharField(max_length=270, null=True, blank=True)
    email           = models.EmailField()
    business_name   = models.CharField(max_length=270, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return 'Signature from %s %s' %(self.first_name, self.last_name)
    
class ArtGallery(models.Model):
    event           = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    title           = models.CharField(max_length=270)
    slug            = models.SlugField(blank=True, null=True)
    items           = models.ManyToManyField(FullGalleryItem, blank=True)
    
    def __str__(self):
        return str(self.title)
    