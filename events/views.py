
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render
from accounts.models import GuestEmail
from addresses.forms import AddressForm, ShippingAddressForm, BillingAddressForm
from addresses.models import Address
from django.template.loader import render_to_string

from billing.models import BillingProfile, Card
from orders.models import Order
from orders.models import Transaction

import braintree
import shippo
import json

from carts.models import GalleryCart, TicketCart, ticketItem, ticketDonation, ticketAd, FullGalleryCart
from .models import *
from django.conf import settings

User = settings.AUTH_USER_MODEL
gateway = settings.GATEWAY

ART_PICKUP_CHOICES = (
    ('Sunday, 11am - 1pm', 'Sunday, 11am - 1pm'),
    ('Sunday, 1pm - 3pm', 'Sunday, 1pm - 3pm'),
    ('Sunday, 3pm - 6pm', 'Sunday, 3pm - 6pm')
)

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
def email_view(request):
    context = {
        'tickets':SingleTicket.objects.filter(last_name='Colon', first_name="Jessica"),
        'event': Event.objects.filter(title='For the Love of Art Juneteenth Celebration'),
    }
    return render(request, 'ticket-email.html', context)
def event_home(request):
    events = Event.objects.all()
    context = {
        'title':'ETV | Events',
        'events': events,
    }
    return render(request, "events-home.html", context)

def event_detail(request, slug):
    event = Event.objects.get(slug=slug)
    context = {
        'title':'ETV | %s' %(event.title),
        'event': event,
    }
    return render(request, "detail.html", context)

def event_ticket_checkout(request, slug):
    event = Event.objects.get(slug=slug)
    ticket_types = TicketType.objects.filter(event=event).filter(sponsorship=False).order_by('price')
    sponsor_types = TicketType.objects.filter(event=event).filter(sponsorship=True).order_by('price')
    (cart_obj) = TicketCart.objects.new_or_get(request, event)
    
    item_list = ticketItem.objects.filter(cart=cart_obj)
    donations = ticketDonation.objects.filter(cart=cart_obj)
    ads = ticketAd.objects.filter(cart=cart_obj)
    ad_types  = AdType.objects.filter(event=event)
    cart_items = list()
    for x in ticket_types:
        ticketType = x
        cartItem = ticketItem.objects.filter(cart=cart_obj).filter(ticket=x).first()
        dictionary = {
            "type": ticketType,
            "cartItem": cartItem,
            "quantity_list": range(0,11)
        }
        cart_items.append(dictionary)
    ad_items = list()
    for x in ad_types:
        adType = x
        adItem = ticketAd.objects.filter(cart=cart_obj).filter(type=x).first()
        dictionary = {
            "type": adType,
            "cartItem": adItem,
        }
        ad_items.append(dictionary)

    cart_sponsor_items = list()
    for x in sponsor_types:
        ticketType = x
        cartItem = ticketItem.objects.filter(cart=cart_obj).filter(ticket=x).first()
        dictionary = {
            "type": ticketType,
            "cartItem": cartItem,
            "quantity_list": range(0,11)
        }
        cart_sponsor_items.append(dictionary)
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
        'title':'ETV | %s' %(event.title),
        'event': event,
        'ads': ads,
        'ticket_types': ticket_types,
        'ad_items': ad_items,
        'ad_types': ad_types,
        'sponsor_types': sponsor_types,
        'item_list': item_list,
        'cart_items': cart_items,
        'cart_sponsor_items': cart_sponsor_items,
        'cart': cart_obj,
        'donations': donations,
        "billing_profile": billing_profile,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "shipping_addresses":shipping_addresses,
        "shipping_id": shipping_address_id,
        "billing_addresses":billing_addresses,
        "states": STATE_CHOICES
    }
    return render(request, "ticket-checkout.html", context)

def event_sponsor_checkout(request, slug):
    event = Event.objects.get(slug=slug)
    ticket_types = TicketType.objects.filter(event=event).filter(sponsorship=False).order_by('price')
    sponsor_types = TicketType.objects.filter(event=event).filter(sponsorship=True).order_by('price')
    (cart_obj) = TicketCart.objects.new_or_get(request, event)
    
    item_list = ticketItem.objects.filter(cart=cart_obj)
    donations = ticketDonation.objects.filter(cart=cart_obj)
    ads = ticketAd.objects.filter(cart=cart_obj)
    ad_types  = AdType.objects.filter(event=event)
    cart_items = list()
    for x in ticket_types:
        ticketType = x
        cartItem = ticketItem.objects.filter(cart=cart_obj).filter(ticket=x).first()
        dictionary = {
            "type": ticketType,
            "cartItem": cartItem,
            "quantity_list": range(0,11)
        }
        cart_items.append(dictionary)
    ad_items = list()
    for x in ad_types:
        adType = x
        adItem = ticketAd.objects.filter(cart=cart_obj).filter(type=x).first()
        dictionary = {
            "type": adType,
            "cartItem": adItem,
        }
        ad_items.append(dictionary)
    cart_items = list()
    for x in ticket_types:
        ticketType = x
        cartItem = ticketItem.objects.filter(cart=cart_obj).filter(ticket=x).first()
        dictionary = {
            "type": ticketType,
            "cartItem": cartItem,
            "quantity_list": range(0,11)
        }
        cart_items.append(dictionary)

    cart_sponsor_items = list()
    for x in sponsor_types:
        ticketType = x
        cartItem = ticketItem.objects.filter(cart=cart_obj).filter(ticket=x).first()
        dictionary = {
            "type": ticketType,
            "cartItem": cartItem,
            "quantity_list": range(0,11)
        }
        cart_sponsor_items.append(dictionary)
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
        'title':'ETV | %s' %(event.title),
        'event': event,
        'ads': ads,
        'ticket_types': ticket_types,
        'ad_items': ad_items,
        'ad_types': ad_types,
        'sponsor_types': sponsor_types,
        'item_list': item_list,
        'cart_items': cart_items,
        'cart_sponsor_items': cart_sponsor_items,
        'cart': cart_obj,
        'donations': donations,
        "billing_profile": billing_profile,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "shipping_addresses":shipping_addresses,
        "shipping_id": shipping_address_id,
        "billing_addresses":billing_addresses,
        "states": STATE_CHOICES
    }
    return render(request, "sponsor-checkout.html", context)

def ticket_cart_ad_update(request):
    type                = request.POST.get('type')
    event_title         = request.POST.get('event')
    ad_id               = request.POST.get('adType')
    ad_type             = AdType.objects.filter(pk=ad_id).first()
    event               = Event.objects.filter(title=event_title).first()
    cart_obj            = TicketCart.objects.new_or_get(request, event)
    data                = {}
    if type == 'add':
        item_obj = ticketAd()
        item_obj.cart = cart_obj
        item_obj.type = ad_type
        item_obj.save()

        price = item_obj.type.price
        event = item_obj.type.event
        data = {
            'price': '$%s' %(price),
            'ad': '%s' %(item_obj.type.title),
            'priceTarget': '.%s-AdPrice' %(item_obj.pk),
            'quantityTarget': '.%s-AdQuantity' %(item_obj.pk),
            'quantity': '1',
            'total': '$%s' %(cart_obj.total),
            'row': '.%s-AdRow' %(item_obj.pk),
            'pk': item_obj.pk,
            'removeContainer': '#%s-remove-container' %(ad_id),
            'typeId': item_obj.type.pk
        }
        return JsonResponse(data)
    elif type == 'remove':
        item_id         = request.POST.get('tid')
        type_id         = request.POST.get('typeId')
        item_obj        = ticketAd(pk=item_id)
        item_obj.delete()
        data = {
            'total': '$%s' %(cart_obj.total),
            'row': '.%s-AdRow' %(item_id),
            'removeContainer': '#%s-remove-container' %(type_id),
            'pk': str(item_id),
            'typeId': str(type_id)
        }
        print(data)
        return JsonResponse(data)
    return JsonResponse(data)

def ticket_cart_donation_update(request):
    event_title         = request.POST.get('event')
    event               = Event.objects.filter(title=event_title).first()
    cart_obj            = TicketCart.objects.new_or_get(request, event)
    amount              = str(request.POST.get('amount'))[2:].replace(',','')
    
    item_obj = ticketDonation()
    item_obj.amount = amount
    item_obj.cart = cart_obj
    item_obj.event = event
    item_obj.save()

    price = item_obj.amount
    event = item_obj.event
    data = {
        'price': '$%s' %(price),
        'priceTarget': '.%s-price' %(item_obj.pk),
        'quantityTarget': '.%s-quantity' %(item_obj.pk),
        'quantity': '1',
        'total': '$%s' %(cart_obj.total),
        'row': '.%s-row' %(item_obj.pk),
        'pk': item_obj.pk,
    }
    return JsonResponse(data)
    
def ticket_cart_donation_remove(request):
    event_title         = request.POST.get('event')
    event               = Event.objects.filter(title=event_title).first()
    cart_obj            = TicketCart.objects.new_or_get(request, event)
    pk                  = request.POST.get('pk')
    
    item_obj = ticketDonation.objects.get(pk=pk)
    item_obj.delete()

    data = {
        'total': '$%s' %(cart_obj.total),
        'row': '.%s-row' %(pk),
        'removeContainer': '#%s-remove-container' %(pk),
        'pk': str(pk)
    }
    return JsonResponse(data)
def ticket_cart_update(request):
    event_title         = request.POST.get('event')
    event               = Event.objects.filter(title=event_title).first()
    cart_obj            = TicketCart.objects.new_or_get(request, event)
    request.session['ticket_cart_id'] = cart_obj.pk
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
    price = int(quantity) * item_obj.ticket.get_price
    event = item_obj.event
    data = {
        'price': '$%s' %(price),
        'priceTarget': '.%s-price' %(item_obj.pk),
        'quantityTarget': '.%s-quantity' %(item_obj.pk),
        'quantity': item_obj.quantity,
        'total': '$%s' %(cart_obj.total),
        'row': '.%s-row' %(item_obj.pk),
        'counter': '.%s-counter' %(item_obj.ticket.pk),
        'previousQuantity': previous_quantity,
        'pk': item_obj.pk,
        'typePk': item_obj.ticket.pk,
        'select': '#%s-counter' %(item_obj.ticket.pk),
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

    putting = TicketType.objects.filter(title='Putting Contest Sponsor').first()
    beverage = TicketType.objects.filter(title='Beverage Station Sponsor').first()
    golfcart = TicketType.objects.filter(title='Golf Cart Sponsor').first()
    tee = TicketType.objects.filter(title='Power Swing Tee Sponsor').first()
    golfergift = TicketType.objects.filter(title='Golfer Gift Sponsor').first()
    reception = TicketType.objects.filter(title='Cocktail Reception Sponsor').first()
    holeinone = TicketType.objects.filter(title='Hole In One Sponsor').first()
    awards = TicketType.objects.filter(title='Awards/Dinner/Banquet Sponsor').first()

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

    putting_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=putting).first()
    beverage_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=beverage).first()
    golfcart_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=golfcart).first()
    tee_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=tee).first()
    golfergift_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=golfergift).first()
    reception_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=reception).first()
    holeinone_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=holeinone).first()
    awards_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=awards).first()

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
    email = object.email
    if request.user.is_authenticated:
        related = SingleTicket.objects.filter(email=email)
        context = {
            'related': related,
            'object': object
        }
    else:
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

    putting = TicketType.objects.filter(title='Putting Contest Sponsor').first()
    beverage = TicketType.objects.filter(title='Beverage Station Sponsor').first()
    golfcart = TicketType.objects.filter(title='Golf Cart Sponsor').first()
    tee = TicketType.objects.filter(title='Power Swing Tee Sponsor').first()
    golfergift = TicketType.objects.filter(title='Golfer Gift Sponsor').first()
    reception = TicketType.objects.filter(title='Cocktail Reception Sponsor').first()
    holeinone = TicketType.objects.filter(title='Hole In One Sponsor').first()
    awards = TicketType.objects.filter(title='Awards/Dinner/Banquet Sponsor').first()

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

    putting_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=putting).first()
    beverage_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=beverage).first()
    golfcart_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=golfcart).first()
    tee_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=tee).first()
    golfergift_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=golfergift).first()
    reception_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=reception).first()
    holeinone_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=holeinone).first()
    awards_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=awards).first()

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

        'putting': putting,
        'beverage': beverage,
        'golfcart': golfcart,
        'tee': tee,
        'golfergift': golfergift,
        'reception': reception,
        'holeinone': holeinone,
        'awards': awards,

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

        'putting_quantity': putting_quantity,
        'beverage_quantity': beverage_quantity,
        'golfcart_quantity': golfcart_quantity,
        'tee_quantity': tee_quantity,
        'golfergift_quantity': golfergift_quantity,
        'reception_quantity': reception_quantity,
        'holeinone_quantity': holeinone_quantity,
        'awards_quantity': awards_quantity,

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

    putting = TicketType.objects.filter(title='Putting Contest Sponsor').first()
    beverage = TicketType.objects.filter(title='Beverage Station Sponsor').first()
    golfcart = TicketType.objects.filter(title='Golf Cart Sponsor').first()
    tee = TicketType.objects.filter(title='Power Swing Tee Sponsor').first()
    golfergift = TicketType.objects.filter(title='Golfer Gift Sponsor').first()
    reception = TicketType.objects.filter(title='Cocktail Reception Sponsor').first()
    holeinone = TicketType.objects.filter(title='Hole In One Sponsor').first()
    awards = TicketType.objects.filter(title='Awards/Dinner/Banquet Sponsor').first()

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

    putting_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=putting).first()
    beverage_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=beverage).first()
    golfcart_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=golfcart).first()
    tee_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=tee).first()
    golfergift_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=golfergift).first()
    reception_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=reception).first()
    holeinone_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=holeinone).first()
    awards_quantity = ticketItem.objects.filter(cart=cart_obj).filter(ticket=awards).first()

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

        'putting': putting,
        'beverage': beverage,
        'golfcart': golfcart,
        'tee': tee,
        'golfergift': golfergift,
        'reception': reception,
        'holeinone': holeinone,
        'awards': awards,

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

        'putting_quantity': putting_quantity,
        'beverage_quantity': beverage_quantity,
        'golfcart_quantity': golfcart_quantity,
        'tee_quantity': tee_quantity,
        'golfergift_quantity': golfergift_quantity,
        'reception_quantity': reception_quantity,
        'holeinone_quantity': holeinone_quantity,
        'awards_quantity': awards_quantity,

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
    donations = ticketDonation.objects.filter(cart=cart_obj).filter(event=event)
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
        'donations': donations,
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

def gallery_home(request):
    cart_obj, created = FullGalleryCart.objects.new_or_get(request)
    items = FullGalleryItem.objects.all().order_by('order', 'artist', 'price')
    artists = Artist.objects.all().order_by('name')
    auction_items = AuctionItem.objects.all()
    p = Paginator(items, 6)
    filter = GalleryFilter(request.GET, queryset=items)
    context = {
        'items': items,
        'p': p,
        'cart': cart_obj,
        'filter': filter,
        'auction_items': auction_items,
        'artists': artists,
    }
    return render(request, 'full_gallery_home.html', context)

def gallery_cart_home(request):
    cart_obj, created = FullGalleryCart.objects.new_or_get(request)
    pickup_options = ART_PICKUP_CHOICES
    context = {
        'cart': cart_obj,
        'pickup_windows': pickup_options,
    }
    return render(request, 'full_gallery_cart.html', context)

def full_gallery_cart_home(request):
    cart_obj, created = FullGalleryCart.objects.new_or_get(request)
    pickup_options = ART_PICKUP_CHOICES
    context = {
        'cart': cart_obj,
        'pickup_windows': pickup_options,
    }
    return render(request, 'full_gallery_cart.html', context)

def full_gallery_home(request):
    cart_obj, created = FullGalleryCart.objects.new_or_get(request)
    items = FullGalleryItem.objects.all().order_by('order', 'artist', 'price')
    artists = Artist.objects.all().order_by('name')
    auction_items = AuctionItem.objects.all()
    p = Paginator(items, 6)
    filter = GalleryFilter(request.GET, queryset=items)
    context = {
        'items': items,
        'p': p,
        'cart': cart_obj,
        'filter': filter,
        'auction_items': auction_items,
        'artists': artists,
    }
    return render(request, 'full_gallery_home.html', context)

def gallery_get_next(request):
    requested_page = request.GET['page']
    items = FullGalleryItem.objects.all().order_by('order', 'artist', 'price')
    p = Paginator(items, 12)
    page = p.get_page(requested_page)
    if page.has_next:
        html = render_to_string('gallery-next.html', {'page': page})
        return HttpResponse(html)
    
def gallery_search(request):
    f = GalleryFilter(request.GET, queryset=FullGalleryItem.objects.all().order_by('order', 'artist', 'price'))
    items = f.qs
    if len(items) > 0:
        p = Paginator(items, 12)
        html = render_to_string('gallery-next.html', {'page': p})
        return HttpResponse(html)
    else:
        return HttpResponse('No Matching Pieces')