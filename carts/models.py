from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils.translation import activate
from events.models import Guest, TicketType
from merchandise.models import *
from django.db.models.signals import pre_save, post_save, m2m_changed
from events.models import Event
User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

    def add_nonce(self, nonce):
        if nonce:
            return self.update(nonce=nonce)
        return None
        
class Cart(models.Model):
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal        = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    total           = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    nonce           = models.CharField(null=True, blank=True, max_length=120)
    total           = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    active          = models.BooleanField(default=True, null=True, blank=True)
    
    objects         = CartManager()

    def __str__(self):
        return  str(self.id)

    @property
    def total(self):
        cart_id = self.id
        qs = list(cartItem.objects.filter(cart=cart_id).all())
        items = qs
        total = 0
        for x in items:
            line_total = x.item.product.price * x.quantity
            total += line_total
        return total

class cartItem(models.Model):
    item        = models.ForeignKey(newInventory, on_delete=models.CASCADE, blank=True, null=True)
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    quantity    = models.IntegerField(default=1)
    product     = models.ForeignKey(newProduct, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.item.sku

    def sub_total(self):
        return self.item.product.price

class TicketCartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("ticket_cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
        else:
            cart_obj = TicketCart.objects.new()
            new_obj = True
            request.session['ticket_cart_id'] = cart_obj.pk
        return cart_obj

    def new(self):
        return self.model.objects.create()

    def add_nonce(self, nonce):
        if nonce:
            return self.update(nonce=nonce)
        return None

class TicketCart(models.Model):
    subtotal        = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    total           = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    nonce           = models.CharField(null=True, blank=True, max_length=120)
    total           = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    active          = models.BooleanField(default=True, null=True, blank=True)
    
    objects         = TicketCartManager()

    @property
    def total(self):
        cart_id = self.id
        qs = list(ticketItem.objects.filter(cart=cart_id).all())
        items = qs
        total = 0
        for x in items:
            line_total = x.ticket.price * x.quantity
            total += line_total
        return total

class ticketItem(models.Model):
    ticket      = models.ForeignKey(TicketType, on_delete=models.SET_NULL, blank=True, null=True)
    cart        = models.ForeignKey(TicketCart, on_delete=models.CASCADE, blank=True, null=True)
    quantity    = models.IntegerField(default=1)
    guests      = models.ManyToManyField(Guest, blank=True)
    event       = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    def subtotal(self):
        return self.ticket.price
    
    @property
    def get_guests(self):
        return range(self.quantity)
    