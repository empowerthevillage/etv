from django.conf import settings
import math
from django.shortcuts import render, redirect
from addresses.models import Address
from billing.models import BillingProfile
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from etv.utils import unique_order_id_generator
from carts.models import Cart, cartItem

import braintree
import shippo
import sweetify

gateway = settings.GATEWAY

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('authorization_expired', 'Authorization Expired'),
    ('authorized', 'Authorized'),
    ('authorizing', 'Authorizing'),
    ('settlement_pending', 'Settlement Pending'),
    ('settlement_declined', 'Settlement Declined'),
    ('failed', 'Failed'),
    ('gateway_rejected', 'Gateway Rejected'),
    ('processor_declined', 'Processor Declined'),
    ('settled', 'Settled'),
    ('settling', 'Settling'),
    ('submitted_for_settlement', 'Submitted For Settlement'),
    ('voided', 'Voided'),
    ('fulfilled', 'Fulfilled'),
)

class OrderManagerQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created =BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')
        
class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

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

class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    braintree_id = models.CharField(max_length=270, blank=True, null=True, verbose_name='ID')
    billing_profile = models.ForeignKey(BillingProfile, models.SET_NULL, null=True, blank=True)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="billing_address", null=True, blank=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="shipping_address", null=True, blank=True)
    payment_method = models.CharField(max_length=270, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(cartItem, blank=True)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    device_data = models.CharField(max_length=270, null=True, blank=True)
    shippo_obj = models.CharField(max_length=270, null=True, blank=True, verbose_name="Shippo ID")
    label = models.URLField(null=True, blank=True, verbose_name="Shipping Label", max_length=1000)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp', '-updated']
    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'django_id': self.order_id})

    @property
    def update_total(self):
        cart_total = self.cart.total
        new_total = cart_total
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total

    @property
    def check_done(self):
        billing_profile = self.billing_profile
        nonce = self.payment_method
        billing_address = self.billing_address
        shipping_address = self.shipping_address
        total = self.total
        if billing_profile and shipping_address and billing_address and nonce and total > 0:
            return True
        return False

    @property
    def charge(self):
        amount = str(self.total)
        nonce = self.payment_method
        result = gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce,
            "device_data": self.device_data,
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success:
            self.status = 'submitted_for_settlement'
        return result

    @property
    def new_label(self):
        shippo.config.api_key = settings.SHIPPO_KEY
        address_from = {
            "name": "Empower The Village",
            "street1": "178 E. Hanover Avenue",
            "street2": "Suite 103-312",
            "city": "Cedar Knolls",
            "state": "NJ",
            "zip": "07927",
            "country": "US"
        }
        
        address_to = {
            "name": self.shipping_address.name,
            "street1": self.shipping_address.address_line_1,
            "street2": self.shipping_address.address_line_2,
            "city": self.shipping_address.city,
            "state": self.shipping_address.state,
            "zip": self.shipping_address.zip_code,
            "country": "US"
        }
        
        parcel = {
            "length": "15.5",
            "width": "12",
            "height": "1",
            "distance_unit": "in",
            "weight": "8",
            "mass_unit": "oz"
        }

        shipment = shippo.Shipment.create(
            address_from = address_from,
            address_to = address_to,
            parcels = [parcel],
        )
        transaction = shippo.Transaction.create(
            shipment = shipment,
            carrier_account = 'de759a0809f44e25bf42756b2ef35685',
            servicelevel_token="usps_parcel_select",
            label_file_type='PDF',
        )
        if transaction.status == "SUCCESS":
            
            return transaction
        else:
            sweetify.error(self.request, 'Address could not be confirmed! Please update shipping address and try again')
            return redirect('/cart')

    @property
    def shipping_details(self):
        shippo.config.api_key = settings.SHIPPO_KEY
        obj = self.shippo_obj
        label = shippo.Transaction.retrieve(obj)
        return label

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)




class OrderRating(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	rating = models.IntegerField(null=True, blank=True)
	verified = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s" %(self.rating)

TRANSACTION_STATUS_CHOICES = (
    ('created', 'Created'),
    ('authorization_expired', 'Authorization Expired'),
    ('authorized', 'Authorized'),
    ('authorizing', 'Authorizing'),
    ('settlement_pending', 'Settlement Pending'),
    ('settlement_declined', 'Settlement Declined'),
    ('failed', 'Failed'),
    ('gateway_rejected', 'Gateway Rejected'),
    ('processor_declined', 'Processor Declined'),
    ('settled', 'Settled'),
    ('settling', 'Settling'),
    ('submitted_for_settlement', 'Submitted For Settlement'),
    ('voided', 'Voided'),
)

class TransactionManagerQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created =BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')
        
class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def add_new(self, billing_profile, cart_obj, nonce):
        created = False
        if nonce:
            amount = cart_obj.total
            nonce = nonce
            transaction_response = gateway.transaction.sale({"amount":amount,"payment_method_nonce":nonce})
            print(transaction_response)
            obj = self.model.objects.create(
                transaction_id=transaction_response.transaction.id,
                status = transaction_response.transaction.status,
                payment_method=nonce,
                billing_profile=billing_profile,
                cart=cart_obj,
                total=amount,)
            created = True
        elif token:
            amount = cart_obj.total
            token = token
            transaction_response = gateway.transaction.sale({"amount":amount,"payment_method_nonce":token})
            obj = self.model.objects.create(
                transaction_id=transaction_response.id,
                status = transaction_response.status,
                payment_method=token,
                billing_profile=billing_profile,
                cart=cart_obj,
                total=amount,)
            created = True
        return obj, created

    def new_or_get(self, billing_profile, cart_obj, nonce):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status='created')
        if qs.count() == 1:
            obj = qs.first()
        elif nonce:
            amount = cart_obj.total
            nonce = nonce
            transaction_response = gateway.transaction.sale({"amount":amount,"payment_method_nonce":nonce})
            print(transaction_response)
            obj = self.model.objects.create(
                transaction_id=transaction_response.transaction.id,
                status = transaction_response.transaction.status,
                payment_method=nonce,
                billing_profile=billing_profile,
                cart=cart_obj,
                total=amount,)
            created = True
        elif token:
            amount = cart_obj.total
            token = token
            transaction_response = gateway.transaction.sale({"amount":amount,"payment_method_nonce":token})
            obj = self.model.objects.create(
                transaction_id=transaction_response.id,
                status = transaction_response.status,
                payment_method=token,
                billing_profile=billing_profile,
                cart=cart_obj,
                total=amount,)
            created = True
        return obj, created

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=120, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(Cart, models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=120, default='created', choices=TRANSACTION_STATUS_CHOICES)
    total = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
            return self.transaction_id

    objects = TransactionManager()

    def update_total(self):
        cart_total = self.cart.total
        new_total = cart_total
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        total = self.total
        if billing_profile and billing_address and total > 0:
            return True
        return False

    def mark_submitted(self):
        if self.check_done():
            self.status = "SubmittedForSettlement"
            self.save()
        return self.status