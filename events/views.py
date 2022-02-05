from django.http.response import JsonResponse
from django.shortcuts import render
from accounts.models import GuestEmail
from addresses.forms import AddressForm, ShippingAddressForm, BillingAddressForm
from addresses.models import Address

from billing.models import BillingProfile, Card
from orders.models import Order
from orders.models import Transaction

import braintree
import shippo

from carts.models import TicketCart, ticketItem
from .models import *
from django.conf import settings

User = settings.AUTH_USER_MODEL
gateway = settings.GATEWAY
STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)
def event_home(request):
    events = Event.objects.all()
    context = {
        'title':'ETV | Events',
        'events': events,
    }
    return render(request, "events-home.html", context)

def ticket_cart_update(request):
    event_title         = request.POST.get('event')
    event               = Event.objects.filter(title=event_title).first()
    cart_obj            = TicketCart.objects.new_or_get(request, event)
    quantity            = request.POST.get('quantity')
    type_id             = request.POST.get('tid')
    item_obj            = ticketItem.objects.filter(cart=cart_obj).filter(ticket=type_id).first()
    previous_quantity   = 0
    if item_obj is not None:
        previous_quantity = item_obj.quantity
        item_obj.quantity = quantity
    else:
        item_obj = ticketItem.objects.create()
        item_obj.quantity = quantity
        item_obj.ticket = TicketType.objects.filter(id=type_id).first()
        item_obj.cart = cart_obj
        item_obj.event = item_obj.ticket.event

    item_obj.save()
    price = int(quantity) * item_obj.ticket.price
    event = item_obj.event
    data = {
        'price': '$%s' %(price),
        'priceTarget': '.%s-price' %(item_obj.pk),
        'quantityTarget': '.%s-quantity' %(item_obj.pk),
        'quantity': item_obj.quantity,
        'total': '$%s' %(cart_obj.total),
        'row': '.%s-row' %(item_obj.pk),
        'previousQuantity': previous_quantity,
        'pk': item_obj.pk,
        'ticket': str(item_obj.ticket)
    }
    return JsonResponse(data)

def ticket_cart_update(request):
    event_title         = request.POST.get('event')
    event               = Event.objects.filter(title=event_title).first()
    cart_obj            = TicketCart.objects.new_or_get(request, event)
    quantity            = request.POST.get('quantity')
    type_id             = request.POST.get('tid')
    item_obj            = ticketItem.objects.filter(cart=cart_obj).filter(ticket=type_id).first()
    previous_quantity   = 0
    if item_obj is not None:
        previous_quantity = item_obj.quantity
        item_obj.quantity = quantity
    else:
        item_obj = ticketItem.objects.create()
        item_obj.quantity = quantity
        item_obj.ticket = TicketType.objects.filter(id=type_id).first()
        item_obj.cart = cart_obj
        item_obj.event = item_obj.ticket.event

    item_obj.save()
    price = int(quantity) * item_obj.ticket.price
    event = item_obj.event
    data = {
        'price': '$%s' %(price),
        'priceTarget': '.%s-price' %(item_obj.pk),
        'quantityTarget': '.%s-quantity' %(item_obj.pk),
        'quantity': item_obj.quantity,
        'total': '$%s' %(cart_obj.total),
        'row': '.%s-row' %(item_obj.pk),
        'previousQuantity': previous_quantity,
        'pk': item_obj.pk,
        'ticket': str(item_obj.ticket)
    }
    return JsonResponse(data)
    
def golf(request):
    event = Event.objects.get(slug='power-swing-classic-golf-event')
    ticket_types = TicketType.objects.filter(event=event)
    single = TicketType.objects.filter(title='Single Golfer').first()
    foursome = TicketType.objects.filter(title='Foursome').first()
    clinic = TicketType.objects.filter(title='Golf Clinic').first()
    mfd = TicketType.objects.filter(title='Member For A Day').first()

    hole = TicketType.objects.filter(title='Hole Sponsor').first()
    bronze = TicketType.objects.filter(title='Bronze/Golf Clinic Sponsor').first()
    silver = TicketType.objects.filter(title='Silver Sponsor').first()
    gold = TicketType.objects.filter(title='Gold Sponsor').first()
    platinum = TicketType.objects.filter(title='Platinum Sponsor').first()
    diamond = TicketType.objects.filter(title='Diamond Sponsor').first()

    (cart_obj) = TicketCart.objects.new_or_get(request, event)
    item_list = ticketItem.objects.filter(cart=cart_obj)
    single_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=single).first()
    foursome_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=foursome).first()
    clinic_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=clinic).first()
    mfd_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=mfd).first()

    hole_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=hole).first()
    bronze_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=bronze).first()
    silver_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=silver).first()
    gold_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=gold).first()
    platinum_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=platinum).first()
    diamond_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=diamond).first()

    billing_address_form = BillingAddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    shipping_addresses = None
    billing_addresses = None
    address_qs = None
    default_card = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            shipping_addresses = address_qs.filter(address_type='shipping')
            billing_addresses = address_qs.filter(address_type='billing')
        
        has_card = billing_profile.has_card
        if has_card:
            default_card = gateway.payment_method.find(billing_profile.default_card.braintree_id)
            for card in billing_profile.get_cards():
                card = gateway.payment_method.find(card.braintree_id)
            customer = gateway.customer.find(billing_profile.customer_id)
            card_qs = customer.credit_cards
        else:
            default_card = None
    context = {
        'title':'ETV | Power Swing Classic',
        'ticket_types': ticket_types,
        'item_list': item_list,
        'cart': cart_obj,
        'hole': hole,
        'bronze': bronze,
        'silver': silver,
        'gold': gold,
        'platinum': platinum,
        'diamond': diamond,

        'single_quantity': single_quantity,
        'foursome_quantity': foursome_quantity,
        'clinic_quantity': clinic_quantity,
        'mfd_quantity': mfd_quantity,

        'hole_quantity': hole_quantity,
        'bronze_quantity': bronze_quantity,
        'silver_quantity': silver_quantity,
        'gold_quantity': gold_quantity,
        'platinum_quantity': platinum_quantity,
        'diamond_quantity': diamond_quantity,

        "billing_profile": billing_profile,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "shipping_addresses":shipping_addresses,
        "shipping_id": shipping_address_id,
        "billing_addresses":billing_addresses,
    }
    return render(request, "golf.html", context)

def art(request):
    event = Event.objects.get(slug='juneteenth-fundraiser')
    ticket_types = TicketType.objects.filter(event=event)
    single = TicketType.objects.filter(title='1-Day Event Pass (Sunday Only)').first()
    saturday = TicketType.objects.filter(title='Saturday VIP Reception').first()
    twoday = TicketType.objects.filter(title='2-Day Event Pass').first()

    bronze = TicketType.objects.filter(title='Bronze Sponsor').filter(event=event).first()
    silver = TicketType.objects.filter(title='Silver Sponsor').filter(event=event).first()
    gold = TicketType.objects.filter(title='Gold Sponsor').filter(event=event).first()
    platinum = TicketType.objects.filter(title='Platinum Sponsor').filter(event=event).first()
    diamond = TicketType.objects.filter(title='Diamond Sponsor').filter(event=event).first()

    (cart_obj) = TicketCart.objects.new_or_get(request, event)
    item_list = ticketItem.objects.filter(cart=cart_obj).filter(event=event)
    single_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=single).first()
    saturday_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=saturday).first()
    twoday_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=twoday).first()

    bronze_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=bronze).first()
    silver_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=silver).first()
    gold_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=gold).first()
    platinum_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=platinum).first()
    diamond_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=diamond).first()
    billing_address_form = BillingAddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    shipping_addresses = None
    billing_addresses = None
    address_qs = None
    default_card = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            shipping_addresses = address_qs.filter(address_type='shipping')
            billing_addresses = address_qs.filter(address_type='billing')
        
        has_card = billing_profile.has_card
        if has_card:
            default_card = gateway.payment_method.find(billing_profile.default_card.braintree_id)
            for card in billing_profile.get_cards():
                card = gateway.payment_method.find(card.braintree_id)
            customer = gateway.customer.find(billing_profile.customer_id)
            card_qs = customer.credit_cards
        else:
            default_card = None

    context = {
        'title':'ETV | For The Love of Art Juneteenth Fundraiser',
        'ticket_types': ticket_types,
        'item_list': item_list,
        'cart': cart_obj,
        'single': single,
        'saturday': saturday,
        'twoday': twoday,
        'bronze': bronze,
        'silver': silver,
        'gold': gold,
        'platinum': platinum,
        'diamond': diamond,
        'single_quantity': single_quantity,
        'saturday_quantity': saturday_quantity,
        'twoday_quantity': twoday_quantity,

        'bronze_quantity': bronze_quantity,
        'silver_quantity': silver_quantity,
        'gold_quantity': gold_quantity,
        'platinum_quantity': platinum_quantity,
        'diamond_quantity': diamond_quantity,

        "billing_profile": billing_profile,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "shipping_addresses":shipping_addresses,
        "shipping_id": shipping_address_id,
        "billing_addresses":billing_addresses,
    }
    return render(request, "juneteenth.html", context)

def ticket(request, ticket_id):
    object = SingleTicket.objects.get(ticket_id=ticket_id)
    context = {
        'object': object,
    }
    return render(request, 'ticket.html', context)

def golf_checkout(request):
    event = Event.objects.get(slug='power-swing-classic-golf-event')
    ticket_types = TicketType.objects.filter(event=event)
    single = TicketType.objects.filter(title='Single Golfer').first()
    foursome = TicketType.objects.filter(title='Foursome').first()
    clinic = TicketType.objects.filter(title='Golf Clinic').first()
    mfd = TicketType.objects.filter(title='Member For A Day').first()

    hole = TicketType.objects.filter(title='Hole Sponsor').first()
    bronze = TicketType.objects.filter(title='Bronze/Golf Clinic Sponsor').first()
    silver = TicketType.objects.filter(title='Silver Sponsor').first()
    gold = TicketType.objects.filter(title='Gold Sponsor').first()
    platinum = TicketType.objects.filter(title='Platinum Sponsor').first()
    diamond = TicketType.objects.filter(title='Diamond Sponsor').first()

    (cart_obj) = TicketCart.objects.new_or_get(request, event)
    item_list = ticketItem.objects.filter(cart=cart_obj)
    single_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=single).first()
    foursome_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=foursome).first()
    clinic_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=clinic).first()
    mfd_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=mfd).first()

    hole_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=hole).first()
    bronze_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=bronze).first()
    silver_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=silver).first()
    gold_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=gold).first()
    platinum_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=platinum).first()
    diamond_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=diamond).first()

    billing_address_form = BillingAddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    shipping_addresses = None
    billing_addresses = None
    address_qs = None
    default_card = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            shipping_addresses = address_qs.filter(address_type='shipping')
            billing_addresses = address_qs.filter(address_type='billing')
        
        has_card = billing_profile.has_card
        if has_card:
            default_card = gateway.payment_method.find(billing_profile.default_card.braintree_id)
            for card in billing_profile.get_cards():
                card = gateway.payment_method.find(card.braintree_id)
            customer = gateway.customer.find(billing_profile.customer_id)
            card_qs = customer.credit_cards
        else:
            default_card = None
    context = {
        'title':'ETV | Power Swing Classic',
        'ticket_types': ticket_types,
        'item_list': item_list,
        'cart': cart_obj,
        'hole': hole,
        'bronze': bronze,
        'silver': silver,
        'gold': gold,
        'platinum': platinum,
        'diamond': diamond,

        'single_quantity': single_quantity,
        'foursome_quantity': foursome_quantity,
        'clinic_quantity': clinic_quantity,
        'mfd_quantity': mfd_quantity,

        'hole_quantity': hole_quantity,
        'bronze_quantity': bronze_quantity,
        'silver_quantity': silver_quantity,
        'gold_quantity': gold_quantity,
        'platinum_quantity': platinum_quantity,
        'diamond_quantity': diamond_quantity,

        "billing_profile": billing_profile,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "shipping_addresses":shipping_addresses,
        "shipping_id": shipping_address_id,
        "billing_addresses":billing_addresses,
        "states": STATE_CHOICES
    }
    return render(request, "golf-ticket-checkout.html", context)

def golf_sponsor_checkout(request):
    event = Event.objects.get(slug='power-swing-classic-golf-event')
    ticket_types = TicketType.objects.filter(event=event)
    single = TicketType.objects.filter(title='Single Golfer').first()
    foursome = TicketType.objects.filter(title='Foursome').first()
    clinic = TicketType.objects.filter(title='Golf Clinic').first()
    mfd = TicketType.objects.filter(title='Member For A Day').first()

    hole = TicketType.objects.filter(title='Hole Sponsor').first()
    bronze = TicketType.objects.filter(title='Bronze/Golf Clinic Sponsor').first()
    silver = TicketType.objects.filter(title='Silver Sponsor').first()
    gold = TicketType.objects.filter(title='Gold Sponsor').first()
    platinum = TicketType.objects.filter(title='Platinum Sponsor').first()
    diamond = TicketType.objects.filter(title='Diamond Sponsor').first()

    (cart_obj) = TicketCart.objects.new_or_get(request, event)
    item_list = ticketItem.objects.filter(cart=cart_obj)
    single_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=single).first()
    foursome_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=foursome).first()
    clinic_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=clinic).first()
    mfd_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=mfd).first()

    hole_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=hole).first()
    bronze_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=bronze).first()
    silver_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=silver).first()
    gold_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=gold).first()
    platinum_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=platinum).first()
    diamond_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=diamond).first()

    billing_address_form = BillingAddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    shipping_addresses = None
    billing_addresses = None
    address_qs = None
    default_card = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            shipping_addresses = address_qs.filter(address_type='shipping')
            billing_addresses = address_qs.filter(address_type='billing')
        
        has_card = billing_profile.has_card
        if has_card:
            default_card = gateway.payment_method.find(billing_profile.default_card.braintree_id)
            for card in billing_profile.get_cards():
                card = gateway.payment_method.find(card.braintree_id)
            customer = gateway.customer.find(billing_profile.customer_id)
            card_qs = customer.credit_cards
        else:
            default_card = None
    context = {
        'title':'ETV | Power Swing Classic',
        'ticket_types': ticket_types,
        'item_list': item_list,
        'cart': cart_obj,
        'hole': hole,
        'bronze': bronze,
        'silver': silver,
        'gold': gold,
        'platinum': platinum,
        'diamond': diamond,

        'single_quantity': single_quantity,
        'foursome_quantity': foursome_quantity,
        'clinic_quantity': clinic_quantity,
        'mfd_quantity': mfd_quantity,

        'hole_quantity': hole_quantity,
        'bronze_quantity': bronze_quantity,
        'silver_quantity': silver_quantity,
        'gold_quantity': gold_quantity,
        'platinum_quantity': platinum_quantity,
        'diamond_quantity': diamond_quantity,

        "billing_profile": billing_profile,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "shipping_addresses":shipping_addresses,
        "shipping_id": shipping_address_id,
        "billing_addresses":billing_addresses,
        "states": STATE_CHOICES
    }
    return render(request, "golf-sponsor-checkout.html", context)

def art_checkout(request):
    event = Event.objects.get(slug='juneteenth-fundraiser')
    ticket_types = TicketType.objects.filter(event=event)
    single = TicketType.objects.filter(title='1-Day Event Pass (Sunday Only)').first()
    saturday = TicketType.objects.filter(title='Saturday VIP Reception').first()
    twoday = TicketType.objects.filter(title='2-Day Event Pass').first()

    bronze = TicketType.objects.filter(title='Bronze Sponsor').filter(event=event).first()
    silver = TicketType.objects.filter(title='Silver Sponsor').filter(event=event).first()
    gold = TicketType.objects.filter(title='Gold Sponsor').filter(event=event).first()
    platinum = TicketType.objects.filter(title='Platinum Sponsor').filter(event=event).first()
    diamond = TicketType.objects.filter(title='Diamond Sponsor').filter(event=event).first()

    (cart_obj) = TicketCart.objects.new_or_get(request, event)
    item_list = ticketItem.objects.filter(cart=cart_obj).filter(event=event)
    single_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=single).first()
    saturday_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=saturday).first()
    twoday_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=twoday).first()

    bronze_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=bronze).first()
    silver_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=silver).first()
    gold_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=gold).first()
    platinum_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=platinum).first()
    diamond_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=diamond).first()
    billing_address_form = BillingAddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    shipping_addresses = None
    billing_addresses = None
    address_qs = None
    default_card = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            shipping_addresses = address_qs.filter(address_type='shipping')
            billing_addresses = address_qs.filter(address_type='billing')
        
        has_card = billing_profile.has_card
        if has_card:
            default_card = gateway.payment_method.find(billing_profile.default_card.braintree_id)
            for card in billing_profile.get_cards():
                card = gateway.payment_method.find(card.braintree_id)
            customer = gateway.customer.find(billing_profile.customer_id)
            card_qs = customer.credit_cards
        else:
            default_card = None

    context = {
        'title':'ETV | For The Love of Art Juneteenth Fundraiser',
        'ticket_types': ticket_types,
        'item_list': item_list,
        'cart': cart_obj,
        'single': single,
        'saturday': saturday,
        'twoday': twoday,
        'bronze': bronze,
        'silver': silver,
        'gold': gold,
        'platinum': platinum,
        'diamond': diamond,
        'single_quantity': single_quantity,
        'saturday_quantity': saturday_quantity,
        'twoday_quantity': twoday_quantity,

        'bronze_quantity': bronze_quantity,
        'silver_quantity': silver_quantity,
        'gold_quantity': gold_quantity,
        'platinum_quantity': platinum_quantity,
        'diamond_quantity': diamond_quantity,

        "billing_profile": billing_profile,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "shipping_addresses":shipping_addresses,
        "shipping_id": shipping_address_id,
        "billing_addresses":billing_addresses,
    }
    return render(request, "art-ticket-checkout.html", context)

def art_sponsor_checkout(request):
    event = Event.objects.get(slug='juneteenth-fundraiser')
    ticket_types = TicketType.objects.filter(event=event)
    single = TicketType.objects.filter(title='1-Day Event Pass (Sunday Only)').first()
    saturday = TicketType.objects.filter(title='Saturday VIP Reception').first()
    twoday = TicketType.objects.filter(title='2-Day Event Pass').first()

    bronze = TicketType.objects.filter(title='Bronze Sponsor').filter(event=event).first()
    silver = TicketType.objects.filter(title='Silver Sponsor').filter(event=event).first()
    gold = TicketType.objects.filter(title='Gold Sponsor').filter(event=event).first()
    platinum = TicketType.objects.filter(title='Platinum Sponsor').filter(event=event).first()
    diamond = TicketType.objects.filter(title='Diamond Sponsor').filter(event=event).first()

    (cart_obj) = TicketCart.objects.new_or_get(request, event)
    item_list = ticketItem.objects.filter(cart=cart_obj).filter(event=event)
    single_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=single).first()
    saturday_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=saturday).first()
    twoday_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=twoday).first()

    bronze_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=bronze).first()
    silver_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=silver).first()
    gold_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=gold).first()
    platinum_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=platinum).first()
    diamond_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=diamond).first()
    billing_address_form = BillingAddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    shipping_addresses = None
    billing_addresses = None
    address_qs = None
    default_card = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            shipping_addresses = address_qs.filter(address_type='shipping')
            billing_addresses = address_qs.filter(address_type='billing')
        
        has_card = billing_profile.has_card
        if has_card:
            default_card = gateway.payment_method.find(billing_profile.default_card.braintree_id)
            for card in billing_profile.get_cards():
                card = gateway.payment_method.find(card.braintree_id)
            customer = gateway.customer.find(billing_profile.customer_id)
            card_qs = customer.credit_cards
        else:
            default_card = None

    context = {
        'title':'ETV | For The Love of Art Juneteenth Fundraiser',
        'ticket_types': ticket_types,
        'item_list': item_list,
        'cart': cart_obj,
        'single': single,
        'saturday': saturday,
        'twoday': twoday,
        'bronze': bronze,
        'silver': silver,
        'gold': gold,
        'platinum': platinum,
        'diamond': diamond,
        'single_quantity': single_quantity,
        'saturday_quantity': saturday_quantity,
        'twoday_quantity': twoday_quantity,

        'bronze_quantity': bronze_quantity,
        'silver_quantity': silver_quantity,
        'gold_quantity': gold_quantity,
        'platinum_quantity': platinum_quantity,
        'diamond_quantity': diamond_quantity,

        "billing_profile": billing_profile,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "shipping_addresses":shipping_addresses,
        "shipping_id": shipping_address_id,
        "billing_addresses":billing_addresses,
    }
    return render(request, "art-sponsor-checkout.html", context)