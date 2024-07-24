from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from billing.models import BillingProfile
from orders.models import Order, LOAPresalePurchase, LOAArtPurchase
from merchandise.models import *
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm, ShippingAddressForm, BillingAddressForm
from addresses.models import Address
from billing.models import BraintreeTransaction
from events.models import *
from donors.models import Donor
from donations.models import donation

import shippo
from django.core.mail import send_mail

from django.core import mail
from django.core.mail import EmailMultiAlternatives

shippo.config.api_key = settings.SHIPPO_KEY
User = settings.AUTH_USER_MODEL
gateway = settings.GATEWAY

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    (items_list) = cartItem.objects.filter(cart=cart_obj)
    products = [{
        "id": x.id,
        "name": x.title,
        "price": x.price,
        "image": x.get_images.first(),
        }
        for x in items_list.all()]
    cart_data = {"products": products, "total": cart_obj.get_total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_items        = cartItem.objects.filter(cart=cart_obj).order_by('product')
    
    context = {
        'cart': cart_obj,
        'items_list': cart_items,
    }
    return render(request, "carts/cart_home.html", context)

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    item_list        = cartItem.objects.filter(cart=cart_obj)
    order_obj = None
    if item_list is None:
        return redirect("cart:home")
    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressForm()
    shipping_address_form = ShippingAddressForm()
    billing_address_form = BillingAddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    shipping_addresses = None
    billing_addresses = None
    address_qs = None
    default_card = None
    card = None
    card_qs = None
    has_card = False
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
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form":login_form,
        "guest_form":guest_form,
        "address_form":address_form,
        "shipping_address_form":shipping_address_form,
        "billing_address_form":billing_address_form,
        "address_qs":address_qs,
        "shipping_addresses":shipping_addresses,
        "shipping_id": shipping_address_id,
        "billing_addresses":billing_addresses,
        "has_card": has_card,
        "default_card": default_card,
        "card": card,
        "card_qs": card_qs,
        "cart": cart_obj,
        'items_list': item_list,
        'tokenization_key': settings.BRAINTREE_TOKENIZATION_KEY,
    }
    
    return render(request, "carts/checkout.html", context)

def ajaxUpdateItems(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    item_list        = cartItem.objects.filter(cart=cart_obj)
    itemID = request.POST.get('itemID')
    newQuantity = request.POST.get('quantity')
    item_obj = cartItem.objects.filter(id=itemID).first()
    item_obj.quantity = newQuantity
    itemPrice = item_obj.item.product.price
    item_obj.save()
    if item_obj.quantity == '0':
        item_obj.delete()
        data = {
            'itemQuantity': 0,
            'cartTotal': cart_obj.get_total,
        }
        return JsonResponse(data)
    else:
        itemTotal = itemPrice * int(item_obj.quantity)
        data = {
            'itemQuantity': item_obj.quantity,
            'cartTotal': cart_obj.get_total,
            'itemTotal': itemTotal,
        }
        return JsonResponse(data)
    

def ajaxRemoveItems(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    itemID = request.POST.get('itemId')
    item_obj = cartItem.objects.filter(id=itemID).first()
    item_obj.quantity = 0
    item_obj.save()
    item_obj.delete()
    data = {
        'cartTotal': cart_obj.get_total
    }
    return JsonResponse(data)

def checkout_new_update(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    email = request.POST.get('email')
    if billing_profile is None:
        request.session['guest_email']=email
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    address_tuple = Address.objects.get_or_create(
        billing_profile = billing_profile,
        address_type = 'shipping',
        name = request.POST.get('name'),
        address_line_1 = request.POST.get('address_line_1'),
        address_line_2 = request.POST.get('address_line_2'),
        city = request.POST.get('city'),
        state = request.POST.get('state'),
        zip_code = request.POST.get('zip'),
    )
    (shipping_address, boolean) = address_tuple
    nonce = request.POST.get('nonce')
    device_data = request.POST.get('deviceData')
    order_obj.device_data = device_data
    order_obj.shipping_address = shipping_address
    order_obj.payment_method = nonce
    order_obj.email = email
    order_obj.save()
    
    request.session["shipping_address_id"] = shipping_address.id
    return redirect("carts:checkout-confirm")
    cart_obj, cart_created = Cart.objects.new_or_get(request)
def checkout_saved_update(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    email = request.POST.get('email')
    shipping_address_id = request.POST.get('shipping_address_id')
    nonce = request.POST.get('nonce')
    device_data = request.POST.get('deviceData')
    order_obj.device_data = device_data
    shipping_address_obj = Address.objects.filter(id=shipping_address_id).first()
    order_obj.shipping_address = shipping_address_obj
    order_obj.payment_method = nonce
    order_obj.email = email
    order_obj.save()
    
    request.session["shipping_address_id"] = order_obj.shipping_address.id
    return redirect("carts:checkout-confirm")

def add_nonce_to_merch(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    email = request.POST.get('email')
    if billing_profile is None:
        request.session['guest_email'] = email
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    shipping_address, created = Address.objects.get_or_create(
        billing_profile = billing_profile,
        address_type = 'shipping',
        name = request.POST.get('name'),
        address_line_1 = request.POST.get('address_line_1'),
        address_line_2 = request.POST.get('address_line_2'),
        city = request.POST.get('city'),
        state = request.POST.get('state'),
        zip_code = request.POST.get('zip'),
    )
    nonce = request.POST.get('nonce')
    device_data = request.POST.get('deviceData')
    order_obj.device_data = device_data
    order_obj.full_name = request.POST.get('name')
    order_obj.shipping_address = shipping_address
    order_obj.payment_method = nonce
    order_obj.total = cart_obj.get_total
    order_obj.email = email
    order_obj.save()
    if order_obj.check_done:
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})
    
def nsnb_update(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    guest_email = request.session.get('guest_email')
    if billing_profile is None:
        email = request.POST.get('email')
        request.session['guest_email'] = email
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    shipping_address_tuple = Address.objects.get_or_create(
        billing_profile = billing_profile,
        address_type = 'shipping',
        name = request.POST.get('ship_name'),
        address_line_1 = request.POST.get('ship_address_line_1'),
        address_line_2 = request.POST.get('ship_address_line_2'),
        city = request.POST.get('ship_city'),
        state = request.POST.get('ship_state'),
        zip_code = request.POST.get('ship_zip'),
    )
    billing_address_tuple = Address.objects.get_or_create(
        billing_profile = billing_profile,
        address_type = 'billing',
        name = request.POST.get('bill_name'),
        address_line_1 = request.POST.get('bill_address_line_1'),
        address_line_2 = request.POST.get('bill_address_line_2'),
        city = request.POST.get('bill_city'),
        state = request.POST.get('bill_state'),
        zip_code = request.POST.get('bill_zip'),
    )
    (shipping_address, boolean) = shipping_address_tuple
    (billing_address, boolean) = billing_address_tuple
    nonce = request.POST.get('nonce')
    device_data = request.POST.get('deviceData')
    order_obj.device_data = device_data
    order_obj.shipping_address = shipping_address
    order_obj.billing_address = billing_address
    order_obj.payment_method = nonce
    order_obj.save()
    
    request.session["shipping_address_id"] = shipping_address.id
    request.session["billing_address_id"] = billing_address.id
    return redirect("carts:checkout-confirm")

def nssb_update(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    billing_address_id = request.POST.get('billing_address_id')
    shipping_address_tuple = Address.objects.get_or_create(
        billing_profile = billing_profile,
        address_type = 'shipping',
        name = request.POST.get('ship_name'),
        address_line_1 = request.POST.get('ship_address_line_1'),
        address_line_2 = request.POST.get('ship_address_line_2'),
        city = request.POST.get('ship_city'),
        state = request.POST.get('ship_state'),
        zip_code = request.POST.get('ship_zip'),
    )
    nonce = request.POST.get('nonce')
    device_data = request.POST.get('deviceData')
    order_obj.device_data = device_data
    (shipping_address, boolean) = shipping_address_tuple
    billing_address_obj = Address.objects.filter(id=billing_address_id).first()
    order_obj.shipping_address = shipping_address
    order_obj.billing_address = billing_address_obj
    order_obj.payment_method = nonce
    order_obj.save()
    
    request.session["shipping_address_id"] = order_obj.shipping_address.id
    request.session["billing_address_id"] = order_obj.billing_address.id
    return redirect("carts:checkout-confirm")

def ssnb_update(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    shipping_address_id = request.POST.get('shipping_address_id')
    billing_address_tuple = Address.objects.get_or_create(
        billing_profile = billing_profile,
        address_type = 'billing',
        name = request.POST.get('bill_name'),
        address_line_1 = request.POST.get('bill_address_line_1'),
        address_line_2 = request.POST.get('bill_address_line_2'),
        city = request.POST.get('bill_city'),
        state = request.POST.get('bill_state'),
        zip_code = request.POST.get('bill_zip'),
    )
    nonce = request.POST.get('nonce')
    device_data = request.POST.get('deviceData')
    order_obj.device_data = device_data
    (billing_address, boolean) = billing_address_tuple
    shipping_address_obj = Address.objects.filter(id=shipping_address_id).first()
    order_obj.shipping_address = shipping_address_obj
    order_obj.billing_address = billing_address
    order_obj.payment_method = nonce
    order_obj.save()
    
    request.session["shipping_address_id"] = order_obj.shipping_address.id
    request.session["billing_address_id"] = order_obj.billing_address.id
    return redirect("carts:checkout-confirm")

def sssb_update(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    shipping_address_id = request.POST.get('shipping_address_id')
    billing_address_id = request.POST.get('billing_address_id')
    nonce = request.POST.get('nonce')
    device_data = request.POST.get('deviceData')
    order_obj.device_data = device_data
    billing_address_obj = Address.objects.filter(id=billing_address_id).first()
    shipping_address_obj = Address.objects.filter(id=shipping_address_id).first()
    order_obj.shipping_address = shipping_address_obj
    order_obj.billing_address = billing_address_obj
    order_obj.payment_method = nonce
    order_obj.save()
    
    request.session["shipping_address_id"] = order_obj.shipping_address.id
    request.session["billing_address_id"] = order_obj.billing_address.id
    return redirect("carts:checkout-confirm")

def checkout_confirm(request):
    try:
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        cart_items        = cartItem.objects.filter(cart=cart_obj)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        for x in cart_items:
            order_obj.items.add(x)
        order_obj.total = cart_obj.get_total
        order_obj.save()
        context = {
            "billing_profile": billing_profile,
            'items_list': cart_items,
            "nonce": gateway.payment_method_nonce.find(order_obj.payment_method),
            "order": order_obj,
            'cart': cart_obj,
            'tokenization_key': settings.BRAINTREE_TOKENIZATION_KEY,
        }
        return render(request, "carts/checkout-confirm.html", context)
    except:
        return redirect('/shop')

def new_charge(request):
    if request.method == 'POST':
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        email = order_obj.email
        if not billing_profile:
            request.session['guest_email'] = email
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        #try:
        amount = str(cart_obj.get_total)
        nonce = str(order_obj.payment_method)
        result = gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce,
            "device_data": request.POST.get('device_data'),
            "customer": {
                "email": email
            },
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success:
            print(order_obj.items.all())
            order_obj.status = 'submitted_for_settlement'
            order_obj.braintree_id = result.transaction.id
            order_obj.save()
            confirmation_subject = 'ETV Merchandise Purchase Confirmation'
            from_email = 'etvnotifications@gmail.com'
            confirmation_content = render_to_string('merchandise-email.html',
            {
                'items': order_obj.items.all(),
            })
            confirmation_plain_text = 'View email in browser'      
            
            send_mail(confirmation_subject, confirmation_plain_text, from_email, [str(email)], html_message=confirmation_content)
            detail_content = render_to_string('merchandise-admin-email.html',
            {
                'purchaser': str(order_obj.full_name),
                'email': order_obj.email,
                'items': order_obj.items.all(),
            })
            
            recipients = ['chandler@eliftcreations.com', 'admin@empowerthevillage.org', 'ayo@empowerthevillage.org']
            #recipients = ['chandler@eliftcreations.com']
            send_mail(
                'New Swag Purchase!',
                str('A new swag purchase has been successfully processed! Purchaser: '+ str(email)),
                'etvnotifications@gmail.com',
                recipients,
                html_message=detail_content,
                fail_silently=True
            )
            status = 'success'
        else:
            status = 'failure'
        data = {
            'status': status,
        }
        return JsonResponse(data)
        #except:
        #    status = 'failure'
        #    data = {
        #        'status': status,
        #        'message': 'Could not create charge'
        #    }
        #    return JsonResponse(data)

def checkout_done(request):
    try:
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        order_obj = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj).first()
        if order_obj is not None:
            del request.session['cart_id']
            context = {
                "order": order_obj,
            }
            return render(request, "carts/checkout-done.html", context)
        else:
            return redirect('/shop')
    except:
        return redirect('/shop')
    
    
def ticket_nb(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is None:
        try:
            email = request.POST.get('guestList[email]')
            request.session['guest_email'] = email
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        except:
            email = request.POST.get('email')
            request.session['guest_email'] = email
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    else:
        email = billing_profile.email
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    event_pk = request.POST.get('event')
    event = Event.objects.filter(pk=event_pk).first()
    cart_obj = TicketCart.objects.new_or_get(request, event)
    amount = str(cart_obj.total)
    nonce = request.POST.get('nonce')
    guest_list = request.POST.get('guestList')
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "device_data": request.POST.get('device_data'),
        "customer": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        },
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        print('Donation succeeded')
        tickets = ticketItem.objects.filter(cart=cart_obj)
        ticket_list = []
        for x in tickets:
            batch_size = x.quantity
            ticket = x.ticket
            price = ticket.get_price
            for i in range(batch_size):
                new_ticket = SingleTicket.objects.create(
                    type=ticket,
                    event=event,
                    billing_profile=billing_profile, 
                    email=email, 
                    first_name=first_name,
                    last_name=last_name,
                    guest_list=guest_list,
                    purchase_price=price,
                    braintree_id=result.transaction.id)
                ticket_list.append(new_ticket)
                try:
                    bt_obj = BraintreeTransaction()
                    bt_obj.braintree_id = new_ticket.braintree_id
                    bt_obj.item = 'Ticket - %s' %(new_ticket.type)
                    bt_obj.purchaser = '%s %s' %(new_ticket.first_name, new_ticket.last_name)
                    bt_obj.amount = new_ticket.purchase_price
                    bt_obj.url = '/dashboard/orders/SingleTicket-list/view/%s' %(new_ticket.pk)
                    bt_obj.save()
                except:
                    pass
        print('Created tickets')
        donor_obj = Donor.objects.filter(first_name=first_name, last_name=last_name).first()
        if donor_obj is None:
            donor_obj = Donor.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
        print('Created donor')
        donations = ticketDonation.objects.filter(cart=cart_obj)
        for x in donations:
            donation_obj = CompleteDonation()
            donation_obj.email = email
            donation_obj.event = event
            donation_obj.billing_profile = billing_profile
            donation_obj.first_name = first_name
            donation_obj.last_name = last_name
            donation_obj.amount = amount
            donation_obj.braintree_id = result.transaction.id
            donation_obj.save()

            donor_obj.event_donations.add(donation_obj)
            donor_obj.save()
        print('Created donations')
        ad_list = []
        ads = ticketAd.objects.filter(cart=cart_obj)
        for x in ads:
            new_ad = Ad.objects.create(
                type=x.type,
                event=event,
                billing_profile=billing_profile, 
                email=email, 
                first_name=first_name,
                last_name=last_name,
            )
            ad_list.append(new_ad)
        print('Created ads')
        cart_obj.active = False
        cart_obj.save()
        confirmation_subject = 'ETV Ticket Purchase Confirmation'
        from_email = 'etvnotifications@gmail.com'
        confirmation_content = render_to_string('ticket-email.html',
        {
            'tickets': ticket_list,
            'ads': ad_list,
            'donations': donations,
            'event': event
        })
        confirmation_plain_text = 'View email in browser'
        print('Created email')   
        
        settings.DEBUG = True
        send_mail(confirmation_subject, confirmation_plain_text, from_email, [str(email)], html_message=confirmation_content, fail_silently=True)
        print('Sent email 1')
        detail_content = render_to_string('ticket-admin-email.html',
        {
            'purchaser': '%s %s' %(first_name, last_name),
            'tickets': ticket_list,
            'ads': ad_list,
            'donations': donations,
            'event': event
        })
        print('Created email 2')
        if event.title == 'Power Swing Classic Fundraiser':
            recipients = ['admin@empowerthevillage.org', 'ayo@empowerthevillage.org', 'powerswing@empowerthevillage.org']
            #recipients = []
        else:
            #recipients = []
            recipients = ['admin@empowerthevillage.org', 'ayo@empowerthevillage.org']
        send_mail(
            'New %s Ticket Purchase' %(event),
            str('A ticket purchase has been successfully processed! Purchaser: '+ str(email)),
            'etvnotifications@gmail.com',
            recipients,
            html_message=detail_content,
            fail_silently=True
        )
        print('Sent email 2')
        settings.DEBUG = False
        return JsonResponse({"status":"success"})
    else:
        print(result)
        return JsonResponse({"status":"error"})

def gallery_cart_update(request):
    itemID = request.POST.get('item')
    item = GalleryItem.objects.get(pk=itemID)
    cart_obj,created = GalleryCart.objects.new_or_get(request)
    if item in cart_obj.items.all():
        status = 'inCart'
    else:
        cart_obj.items.add(item)
        status = 'success'
    response = {
        'status': status,
        'count': len(cart_obj.items.all()),
        'pk': item.pk
    }
    return JsonResponse(response)

def gallery_cart_remove(request):
    itemID = request.POST.get('item')
    item = GalleryItem.objects.get(pk=itemID)
    cart_obj,created = GalleryCart.objects.new_or_get(request)
    if item in cart_obj.items.all():
        cart_obj.items.remove(item)
        status = 'success'
    else:
        status = 'error'
    response = {
        'status': status,
        'count': len(cart_obj.items.all()),
        'pk': item.pk,
        'total': cart_obj.total
    }
    return JsonResponse(response)

def gallery_sale(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is None:
        email = request.POST.get('email')
        request.session['guest_email'] = email
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    else:
        email = billing_profile.email
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    cart_obj, created = GalleryCart.objects.new_or_get(request)
    amount = str(cart_obj.total)
    nonce = request.POST.get('nonce')

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "device_data": request.POST.get('device_data'),
        "customer": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        },
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        items = cart_obj.items.all()
        order_obj = LOAPresalePurchase()
        order_obj.braintree_id = result.transaction.id
        order_obj.first_name = first_name
        order_obj.last_name = last_name
        order_obj.total = amount
        order_obj.save()
        for x in items:
            x.sold = True
            x.save()
            order_obj.items.add(x)
            order_obj.save()
        
        cart_obj.active = False
        cart_obj.save()
        confirmation_subject = 'ETV Art Purchase Confirmation'
        from_email = 'etvnotifications@gmail.com'
        confirmation_content = render_to_string('presale-email.html',
        {
            'items': items,
        })
        confirmation_plain_text = 'View email in browser'      
        
        send_mail(confirmation_subject, confirmation_plain_text, from_email, [str(email)], html_message=confirmation_content)
        detail_content = render_to_string('presale-admin-email.html',
        {
            'purchaser': '%s %s' %(first_name, last_name),
            'items': items,
        })
        
        recipients = ['chandler@eliftcreations.com', 'admin@empowerthevillage.org', 'ayo@empowerthevillage.org']
        #recipients = ['chandler@eliftcreations.com']
        send_mail(
            'New Art Purchase!',
            str('A new artwork purchase has been successfully processed! Purchaser: '+ str(email)),
            'etvnotifications@gmail.com',
            recipients,
            html_message=detail_content,
            fail_silently=True
        )
        status = 'success'
    else:
        status = 'failure'
    message = result.transaction.processor_response_text
    data = {
        'status': status,
        'message': message
    }
    return JsonResponse(data)

def full_gallery_cart_update(request):
    itemID = request.POST.get('item')
    item = FullGalleryItem.objects.get(pk=itemID)
    cart_obj,created = FullGalleryCart.objects.new_or_get(request)
    if item in cart_obj.items.all():
        status = 'inCart'
    else:
        cart_obj.items.add(item)
        status = 'success'
    response = {
        'status': status,
        'count': len(cart_obj.items.all()),
        'pk': item.pk
    }
    return JsonResponse(response)

def full_gallery_cart_remove(request):
    itemID = request.POST.get('item')
    item = FullGalleryItem.objects.get(pk=itemID)
    cart_obj,created = FullGalleryCart.objects.new_or_get(request)
    if item in cart_obj.items.all():
        cart_obj.items.remove(item)
        status = 'success'
    else:
        status = 'error'
    response = {
        'status': status,
        'count': len(cart_obj.items.all()),
        'pk': item.pk,
        'total': cart_obj.total
    }
    return JsonResponse(response)

def full_gallery_sale(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is None:
        email = request.POST.get('email')
        request.session['guest_email'] = email
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    else:
        email = billing_profile.email
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    cart_obj, created = FullGalleryCart.objects.new_or_get(request)
    amount = str(cart_obj.total)
    nonce = request.POST.get('nonce')
    
    if request.POST.get('shipped') == 'True':
        shipped = True
        shipping_name = request.POST.get('address_data[1][value]')
        shipping_address_1 = request.POST.get('address_data[2][value]')
        shipping_address_2 = request.POST.get('address_data[3][value]')
        shipping_city = request.POST.get('address_data[4][value]')
        shipping_state = request.POST.get('address_data[5][value]')
        shipping_zip = request.POST.get('address_data[6]][value]')
    else:
        shipped = False
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "device_data": request.POST.get('device_data'),
        "customer": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        },
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        items = cart_obj.items.all()
        order_obj = LOAArtPurchase()
        order_obj.braintree_id = result.transaction.id
        order_obj.first_name = first_name
        order_obj.last_name = last_name
        order_obj.email = email
        order_obj.phone = phone
        order_obj.total = amount
        if shipped == True:
            order_obj.shipping_requested = True
            order_obj.shipping_address_name = shipping_name
            order_obj.shipping_address_line_1 = shipping_address_1
            order_obj.shipping_address_line_2 = shipping_address_2
            order_obj.shipping_address_city = shipping_city
            order_obj.shipping_address_state = shipping_state
            order_obj.shipping_address_zip = shipping_zip
        order_obj.save()
        for x in items:
            x.sold = True
            x.save()
            order_obj.items.add(x)
            order_obj.save()
        
        cart_obj.active = False
        cart_obj.save()
        confirmation_subject = "ETV Art Gallery Purchase Confirmation"
        from_email = 'etvnotifications@gmail.com'
        confirmation_content = render_to_string('art-email.html',
        {
            'items': items,
            'shipped': shipped,
            'order': order_obj
        })
        confirmation_plain_text = 'View email in browser'      
        
        send_mail(confirmation_subject, confirmation_plain_text, from_email, [str(email)], html_message=confirmation_content)
        detail_content = render_to_string('art-admin-email.html',
        {
            'purchaser': '%s %s' %(first_name, last_name),
            'email': email,
            'phone': phone,
            'items': items,
            'shipped': shipped,
            'order': order_obj
        })
        
        recipients = ['chandler@eliftcreations.com', 'shannon@empowerthevillage.org', 'admin@empowerthevillage.org', 'ayo@empowerthevillage.org']
        #recipients = ['chandler@eliftcreations.com']
        item_string = ''
        try:
            for x in items:
                item_string += str(x.title)
        except:
            pass
        send_mail(
            'New Art Show Purchase!',
            str('An art piece purchase has been successfully processed! Purchaser: '+ str(email)+' Items: '+ str(item_string)),
            'etvnotifications@gmail.com',
            recipients,
            html_message=detail_content,
            fail_silently=True
        )
        status = 'success'
    else:
        status = 'failure'
    message = result.transaction.processor_response_text
    data = {
        'status': status,
        'message': message
    }
    return JsonResponse(data)

def gallery_make_disbursement(request):
    purchases = LOAArtPurchase.objects.all()
    for x in purchases:
        try:
            bt_obj = BraintreeTransaction()
            bt_obj.braintree_id = x.braintree_id
            objs = []
            for piece in x.items.all():
                objs.append('%s by %s' %(piece.title, piece.artist))
            string = ' | '.join(objs)
            bt_obj.item = 'Art Purchase - %s' %(string)
            bt_obj.purchaser = '%s %s' %(x.first_name, x.last_name)
            bt_obj.amount = x.total
            bt_obj.save()
        except:
            pass
        
    return HttpResponse('success')

def donation_make_disbursement(request):
    donations = donation.objects.all()
    for x in donations:
        try:
            bt_obj = BraintreeTransaction()
            bt_obj.braintree_id = x.braintree_id
            bt_obj.item = 'Donation'
            bt_obj.purchaser = '%s %s' %(x.first_name, x.last_name)
            bt_obj.amount = x.amount
            bt_obj.save()
            
        except:
            pass
        
    return HttpResponse('success')