
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
from django.http.response import JsonResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from addresses.forms import BillingAddressForm
from addresses.models import Address
from django.template.loader import render_to_string

from billing.models import BillingProfile
import sweetify

from carts.models import TicketCart, ticketItem, ticketDonation, ticketAd, FullGalleryCart
from .models import *
from django.conf import settings
from orders.models import LOAArtPurchase, SilentAuctionPurchase

from mailchimp_marketing import Client

mailchimp = Client()
mailchimp.set_config({
    "api_key": settings.MAILCHIMP_API_KEY,
    "server": "us7"
})

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
        'tickets':SingleTicket.objects.filter(braintree_id="g5dywchd"),
        'event': Event.objects.filter(title='Empowerment Expo'),
    }
    return render(request, 'ticket-email.html', context)

def art_email_view(request):
    order = LOAArtPurchase.objects.filter(braintree_id="n91d5jmg").first()
    context = {
        'items': order.items.all,
        'shipped': False,
        'order': order,
    }
    return render(request, "art-email.html", context)

def event_home(request):
    context = {
        'title':'ETV | Events',
    }
    return render(request, "events-home.html", context)

def event_detail(request, slug):
    if slug == 'friends-of-the-village-art-exhibition':
        return HttpResponseNotFound("Oops! The event you're looking for is no longer available")
    else:
        event = Event.objects.get(slug=slug)
        context = {
            'title':'ETV | %s' %(event.title),
            'event': event,
        }
        return render(request, "detail.html", context)

def event_ticket_checkout(request, slug):
    event = Event.objects.get(slug=slug)
    ticket_types = TicketType.objects.filter(event=event).filter(sponsorship=False).filter(active=True).order_by('order', 'price')
    sponsor_types = TicketType.objects.filter(event=event).filter(sponsorship=True).filter(active=True).order_by('order', 'price')
    (cart_obj) = TicketCart.objects.new_or_get(request, event)
    
    item_list = ticketItem.objects.filter(cart=cart_obj)
    donations = ticketDonation.objects.filter(cart=cart_obj)
    ads = ticketAd.objects.filter(cart=cart_obj)
    ad_types  = AdType.objects.filter(event=event)
    quantity_list = range(0,11)
    cart_items = list()
    for x in ticket_types:
        ticketType = x
        if x.qty_limit > 0:
            upper_lim = x.qty_limit + 1
            quantity_list = range(0, upper_lim)
        else:
            quantity_list = range(0,11)
        cartItem = ticketItem.objects.filter(cart=cart_obj).filter(ticket=x).first()
        dictionary = {
            "type": ticketType,
            "cartItem": cartItem,
            "quantity_list": quantity_list
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
    ticket_qty = len(ad_items) + len(cart_items) + len(cart_sponsor_items)
    context = {
        'ticket_qty': ticket_qty,
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
        "states": STATE_CHOICES,
        'tokenization_key': settings.BRAINTREE_TOKENIZATION_KEY,
    }
    return render(request, "ticket-checkout.html", context)

def event_sponsor_checkout(request, slug):
    event = Event.objects.get(slug=slug)
    ticket_types = TicketType.objects.filter(event=event).filter(sponsorship=False).filter(active=True).order_by('order','price')
    sponsor_types = TicketType.objects.filter(event=event).filter(sponsorship=True).filter(active=True).order_by('order','price')
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
        "states": STATE_CHOICES,
        'tokenization_key': settings.BRAINTREE_TOKENIZATION_KEY
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
        related = SingleTicket.objects.filter(email=email).filter(checked_in=False)
        if len(related) == 0:
            related = [object]
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
    items = FullGalleryItem.objects.filter(active=True)[:12]
    artists = Artist.objects.filter(active=True).order_by('name')
    auction_items = AuctionItem.objects.all()
    p = Paginator(items, 6)
    filter = GalleryFilter(request.GET, queryset=items)
    context = {
        'items': items,
        'cart': cart_obj,
        'filter': filter,
        'auction_items': auction_items,
        'artists': artists,
    }
    return render(request, 'full_gallery_home.html', context)

def gallery_cart_home(request):
    cart_obj, created = FullGalleryCart.objects.new_or_get(request)
    context = {
        'cart': cart_obj,
        'state_options': STATE_CHOICES,
    }
    return render(request, 'full_gallery_cart.html', context)

def full_gallery_cart_home(request):
    cart_obj, created = FullGalleryCart.objects.new_or_get(request)
    context = {
        'cart': cart_obj,
        'state_options': STATE_CHOICES,
        'tokenization_key': settings.BRAINTREE_TOKENIZATION_KEY
    }
    return render(request, 'mv_full_gallery_cart.html', context)

def full_gallery_home(request):
    cart_obj, created = FullGalleryCart.objects.new_or_get(request)
    items = FullGalleryItem.objects.filter(active=True).order_by('sold', 'artist', 'title')[:12]
    artists = Artist.objects.filter(active=True).order_by('name')
    filter = GalleryFilter(request.GET, queryset=items)
    context = {
        'items': items,
        'cart': cart_obj,
        'filter': filter,
        'artists': artists,
    }
    return render(request, 'mv_gallery_home.html', context)
    #return HttpResponseNotFound("Oops! The event you're looking for is no longer available")

def gallery_get_next(request):
    requested_page = request.GET['next_page']
    items = FullGalleryItem.objects.filter(active=True).order_by('sold', 'artist', 'title')
    p = Paginator(items, 12)
    next_page = int(requested_page) + 1
    page = p.get_page(requested_page)
    if page.has_next():
        html = render_to_string('gallery-next.html', {'page': page, 'error_msg': None})
    elif next_page == p.num_pages + 1:
        html = render_to_string('gallery-next.html', {'page': page, 'error_msg': None})
    else:
        html = render_to_string('gallery-next.html', {'error_msg': True, 'message': 'End of Gallery'})
    return HttpResponse(html)

def gallery_search_available(request):
    try:
        availability = request.GET['availability']
        if availability == 'available':
            availability = False
        elif availability == 'sold':
            availability = True
    except:
        availability = None
    try:
        title = request.GET['title']
    except:
        title = None
        
    if title and availability is not None:
        items = FullGalleryItem.objects.filter(Q(title__icontains=title) & Q(sold=availability) & Q(active=True))
    
    elif title:
        items = FullGalleryItem.objects.filter(Q(title__icontains=title) & Q(active=True))
        
    elif availability is not None:
        items = FullGalleryItem.objects.filter(Q(sold=availability) & Q(active=True))
    
    if len(items) > 0:
        p = Paginator(items, 24)
        html = render_to_string('gallery-next.html', {'page': p.get_page(1), 'error_msg': None})
        return HttpResponse(html)
    else:
        html = render_to_string('gallery-next.html', {'error_msg': True, 'message': 'No Matching Pieces Found', 'page': None})
        return HttpResponse(html)
    
def gallery_search(request):
    try:
        title = request.GET['title']
    except:
        title = None
    try:
        artist = request.GET['artist']
    except:
        artist = None
    if title and artist:
        items = FullGalleryItem.objects.filter(Q(title__icontains=title) & Q(artist__icontains=artist) & Q(active=True))
    elif title:
        items = FullGalleryItem.objects.filter(Q(title__icontains=title) & Q(active=True))
    elif artist:
        items = FullGalleryItem.objects.filter(Q(artist__icontains=artist) & Q(active=True))

    if len(items) > 0:
        p = Paginator(items, 24)
        html = render_to_string('gallery-next.html', {'page': p.get_page(1), 'error_msg': None})
        return HttpResponse(html)
    else:
        html = render_to_string('gallery-next.html', {'error_msg': True, 'message': 'No Matching Pieces Found', 'page': None})
        return HttpResponse(html)
    
def checkin(request):
    if request.method == 'POST':
        tickets = request.POST.getlist('ticket')
        first = SingleTicket.objects.get(ticket_id=tickets[0])
        checkin = CheckIn()
        checkin.first_name = first.first_name
        checkin.last_name = first.last_name
        checkin.email = first.email
        try:
            checkin.guests = int(request.POST.get('guest-qty'))
        except:
            checkin.guests = 0
        checkin.guest_list = request.POST.get('guest-list')
        checkin.save()
        for x in tickets:
            ticket = SingleTicket.objects.get(ticket_id = x)
            ticket.checked_in = True
            ticket.save()
            checkin.tickets.add(ticket)
            
        sweetify.success(request, title='Success!', icon='success', text="Check in successful!", button='OK', timer=10000)
        return redirect('/events/check-in-success/')
           
def new_checkin(request):
    f = TicketFilter(request.GET, queryset=SingleTicket.objects.filter(checked_in=False))
    items = f.qs
    context = {
        'f': f,
        'items': items,
    }
    return render(request, 'check-in-home.html', context)

def ticket_search(request):
    if request.method == 'POST':
        f = TicketFilter(request.POST, queryset=SingleTicket.objects.all())
        items = f.qs
        if len(items) > 0:
            first = items.first()
            path = '/events/ticket/%s/' %(first.ticket_id)
            return redirect(path)
        else:
            sweetify.error('Ticket not found')
            return HttpResponse('Ticket not found')
        
def checkin_success(request):
    return render(request, 'check-in-success.html')

def view_checkins(request):
    checkins = CheckIn.objects.filter(active=True)
    context = {
        'checkins': checkins
    }
    return render(request, 'view-checkins.html', context)

def pitch_registration(request):
    return render(request, 'pitch-registration-2024.html')

def pitch_rules_agreement(request):
    if request.method == 'POST':
        obj = Signature()
        obj.purpose = 'Agreed to 2024 Empowerment Expo Village Ventures Rules & Terms'
        obj.first_name = request.POST['first-name']
        obj.last_name = request.POST['last-name']
        obj.email = request.POST['email']
        obj.business_name = request.POST['business']
        obj.save()
    return HttpResponse('success')

def custom_gallery(request, slug):
    cart_obj, created = FullGalleryCart.objects.new_or_get(request)
    #try:
    gallery_obj = ArtGallery.objects.get(slug=slug)
    gallery_items = gallery_obj.items.filter(active=True)
    context = {
        'items': gallery_items,
        'cart': cart_obj,
        'gallery': gallery_obj,
    }
    return render(request, 'custom-gallery.html', context)
    #except:
    #    return redirect('/events/')

def silent_auction(request):
    items = AuctionItem.objects.filter(active=True)
    context = {
        'items': items,
    }
    return render(request, 'power-swing-silent-auction.html', context)

def silent_auction_buy_now(request, item_id):
    item = AuctionItem.objects.get(item_id=item_id)
    tokenization_key = settings.BRAINTREE_TOKENIZATION_KEY
    context = {
        'item': item,
        'tokenization_key': tokenization_key,
        'mailing_form': BillingAddressForm(),
    }
    return render(request, 'silent-auction-checkout.html', context)

def process_silent_auction_purchase(request):
    if request.method == 'POST':
        data = request.POST
        nonce_id = data['nonce']
        first_name = data['first_name']
        last_name = data['last_name']
        item_pk = data['item_pk']
        item_obj = AuctionItem.objects.get(pk=item_pk)
        email = data['email']
        total = data['amount']
        result = gateway.transaction.sale({
            "amount": total,
            "payment_method_nonce": nonce_id,
            "customer": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            },
            "custom_fields": {
                "memo": 'Power Swing Silent Auction Purchase - %s' %(item_obj)
            },
            "options": {
                "submit_for_settlement": True,
            },
        })
        if result.is_success:
            merge_fields = {
                "FNAME": str(first_name),
                "ETVAMOUNT": str(total)
            }
            mailchimp.lists.set_list_member("bfb104d810", email, {"email_address": email, "status_if_new": "subscribed", "merge_fields": merge_fields})
            mailchimp.customerJourneys.trigger(2794, 15013, {"email_address": str(email)})
            send_mail(
                'New Silent Auction Purchase!',
                str('A new silent auction for %s has been received from %s %s through www.empowerthevillage.org!' %(item_obj, first_name, last_name)),
                'etvnotifications@gmail.com',
                ['admin@empowerthevillage.org', 'chandler@eliftcreations.com', 'ayo@empowerthevillage.org'],
                #['chandler@eliftcreations.com'],
                fail_silently=True
            )
            order_obj = SilentAuctionPurchase()
            order_obj.first_name = first_name
            order_obj.last_name = last_name
            order_obj.item = item_obj
            order_obj.email = email
            order_obj.phone = data['phone']
            order_obj.braintree_id = result.transaction.id
            order_obj.amount = total
            order_obj.save()
            item_obj.sold = True
            item_obj.save()
            
            data = {
                    'status': 'success',
                    'html': render_to_string('silent-auction-buy-now-success.html', context={'purchase': order_obj,
                        'payment_method': result.transaction.credit_card_details,
                        'item': item_obj,
                    })
            }
            return JsonResponse(data)
        else:
            data = {
                'status': 'error',
                'message': 'There was an issue processing your payment method. Please verify your card details and try again'
            }
            return JsonResponse(data)
        
def berg_marketplace(request):
    return render(request, 'berg-marketplace.html')

def free_registration(request, slug):
    if request.method == 'POST':
        try:
            event = Event.objects.filter(slug=slug).first()
            reg_obj_temp = FreeRegistrationTemplate.objects.filter(event=event).first()
            data = request.POST
            reg_obj = FreeRegistration()
            reg_obj.event = reg_obj_temp
            reg_obj.first_name = data['fname']
            reg_obj.last_name = data['lname']
            reg_obj.email = data['email']
            reg_obj.guest_list = data['guest-list']
            reg_obj.affiliation = data['affiliation']
            reg_obj.save()
            try:
                from_email = 'etvnotifications@gmail.com'
                registrant_subject = "Free Registration for ETV's %s Confirmed!" %(event)
                registrant_content = render_to_string('free-reg-email.html',
                {
                })
                registrant_plain_text = 'View email in browser'      
                send_mail(registrant_subject, registrant_plain_text, from_email, [str(reg_obj.email)], html_message=registrant_content)
                
                confirmation_subject = 'New %s Free Registration!' %(reg_obj_temp)
                
                confirmation_content = render_to_string('new-free-reg.html',
                {
                    'obj': reg_obj,
                    'template': reg_obj_temp
                })
                confirmation_plain_text = 'View email in browser'      
                send_mail(confirmation_subject, confirmation_plain_text, from_email, ['chandler@eliftcreations.com', 'ayo@empowerthevillage.org', 'admin@empowerthevillage.org'], html_message=confirmation_content)
            except:
                pass
            #send_mail(confirmation_subject, confirmation_plain_text, from_email, ['chandler@eliftcreations.com'], html_message=confirmation_content)

            sweetify.success(request, title='Success!', icon='success', text="You're registered for the Expo!", button='OK', timer=20000)
            return redirect(event.get_absolute_url())
        except:
            sweetify.error('Please make sure all required fields are valid and try again')
    else:
        event = Event.objects.filter(slug=slug).first()
        reg_obj = FreeRegistrationTemplate.objects.filter(event=event).first()
        context = {
            'event': event,
            'reg_obj': reg_obj,
        }
        return render(request, 'free-registration.html', context)