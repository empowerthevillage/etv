from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from etv.utils import unique_subscription_id_generator
from accounts.models import GuestEmail

import braintree

User = settings.AUTH_USER_MODEL
gateway = settings.GATEWAY

PAYMENT_FEE_CHOICES = (
    ('card', 'Card'),
    ('paypal', 'PayPal')
)
class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email = request.session.get('guest_email')
        created = False
        obj = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(
            user=user,
            email=user.email)

        elif guest_email is not None:
            guest_email_obj, created = GuestEmail.objects.get_or_create(email=guest_email)
            obj, created = self.model.objects.get_or_create(
            email=guest_email_obj.email)
        else:
            pass
        return obj, created

class BillingProfile(models.Model):
    user        = models.OneToOneField(User, models.SET_NULL, null=True, blank=True)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    first_name  = models.CharField(max_length=120, null=True, blank=True)
    last_name   = models.CharField(max_length=120, null=True, blank=True)
    objects = BillingProfileManager()

    def __str__(self):
        return str(self.email)

    def charge(self, billing_profile, order_obj, card=None):
        return Charge.objects.do(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse('billing-payment-method')

    @property
    def has_card(self):
        instance = self
        card_qs = instance.get_cards()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()

def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = gateway.customer.create({
            "email":instance.email,
            "first_name":instance.first_name,
            "last_name":instance.last_name,
        })
        instance.customer_id = customer.customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)

class CardManager(models.Manager):
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, nonce):
        if nonce:
            customer = billing_profile.customer_id
            braintree_card_response = gateway.payment_method.create({"customer_id":customer,"payment_method_nonce":nonce})
            new_card = self.model(
                billing_profile=billing_profile,
                braintree_id = braintree_card_response.payment_method.token,
            )
            new_card.save()
            return new_card
        return None

class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    braintree_id = models.CharField(max_length=120, null=True, blank=True)
    default = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CardManager()
    def __str__(self):
        return self.braintree_id

def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)

post_save.connect(new_card_post_save_receiver, sender=Card)

class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No Cards Available"
        pass

class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    braintree_id = models.CharField(max_length=120)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()

class SubscriptionManager(models.Manager):
    def all(self, *args, **kwargs):
        return self.get_queryset()

class Subscription(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    plan_id = models.CharField(max_length=120)
    payment_token = models.CharField(max_length=120)
    braintree_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.braintree_id

def subscription_create_id(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        instance.braintree_id = unique_subscription_id_generator(instance)

pre_save.connect(subscription_create_id, sender=Subscription)

def subscription_vault_create(sender, instance, *args, **kwargs):
    payment_token = instance.payment_token
    plan_id = instance.plan_id
    braintree_id = instance.braintree_id
    gateway.subscription.create({"payment_method_token":payment_token,"plan_id":plan_id,"id":braintree_id})

post_save.connect(subscription_vault_create, sender=Subscription)

class BraintreeTransaction(models.Model):
    braintree_id = models.CharField(max_length=50, null=True)
    item = models.CharField(max_length=270)
    purchaser = models.CharField(max_length=270)
    amount = models.DecimalField(max_digits=200, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_FEE_CHOICES, null=True)
    url = models.CharField(max_length=270, null=True)
    
    def __str__(self):
        return str(self.braintree_id)
    
    class Meta:
        ordering = ['-amount']

class Disbursement(models.Model):
    disbursement_date = models.DateField(null=True, blank=True)
    disbursement_id = models.CharField(max_length=270, null=True, blank=True)
    transactions = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.disbursement_date)
    
    class Meta:
        ordering = ['-disbursement_date']

    @property
    def get_data(self):
        line_item = {"date": self.disbursement_date, "transactions": {}}
        transaction_ids = self.transactions.strip('][').split(',')
        transaction_count = len(transaction_ids)
        list = []
        total_list = []
        fees_list = [0.49*transaction_count]
        net_list = []
        items = []
        for x in transaction_ids:
            x = str(x).strip("'")
            x = str(x).strip(" '")
            list.append(x)
            transactions = BraintreeTransaction.objects.filter(braintree_id=x)
            for x in transactions:
                items.append(x)
                total_list.append(x.amount)
                if x.payment_method == 'card':
                    fee = float(x.amount) * 0.0199
                    fees_list.append(fee)
                elif x.payment_method == 'paypal':
                    fee = float(x.amount) * 0.0349
                    fees_list.append(fee)
                else:
                    fee = float(x.amount) * 0.0199
                    fees_list.append(fee)
                net_list.append(float(x.amount) - fee)
        total = {"gross": sum(total_list)}
        fees = {"fees": sum(fees_list)}
        net = {"net": float(sum(total_list)) - sum(fees_list)}
        transaction_list = {"transactions": list}
        item_list = {"items": items}
        line_item.update(total)
        line_item.update(fees)
        line_item.update(net)
        line_item.update(item_list)
        line_item.update(transaction_list)
        return line_item
        