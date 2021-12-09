from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from billing.models import BillingProfile, Card
from orders.models import Order
from orders.models import Transaction
from merchandise.models import *
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm, ShippingAddressForm, BillingAddressForm
from addresses.models import Address

import braintree
import shippo

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
    cart_data = {"products": products, "total": cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_items        = cartItem.objects.filter(cart=cart_obj).order_by('product')
    
    context = {
        'cart': cart_obj,
        'items_list': cart_items,
    }
    return render(request, "carts/cart_home.html", context)

def cart_update(request):
    item_id = request.POST.get('item_id')

    if item_id is not None:
        try:
            item_obj = item.objects.get(id=item_id)
        except item.DoesNotExist:
            return redirect("merchandise:list")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if item_obj in cart_obj.products.all():
            cart_obj.products.remove(item_obj)
            added = False
        else:
            cart_obj.products.add(item_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count(),
            }
            return JsonResponse(json_data)
    return redirect('merchandise:list')

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
        'items_list': item_list
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
            'cartTotal': cart_obj.total,
        }
        return JsonResponse(data)
    else:
        itemTotal = itemPrice * int(item_obj.quantity)
        data = {
            'itemQuantity': item_obj.quantity,
            'cartTotal': cart_obj.total,
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
        'cartTotal': cart_obj.total
    }
    return JsonResponse(data)

def checkout_new_update(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is None:
        email = request.POST.get('email')
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
    order_obj.save()
    
    request.session["shipping_address_id"] = shipping_address.id
    return redirect("carts:checkout-confirm")
    cart_obj, cart_created = Cart.objects.new_or_get(request)
def checkout_saved_update(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    
    shipping_address_id = request.POST.get('shipping_address_id')
    nonce = request.POST.get('nonce')
    device_data = request.POST.get('deviceData')
    order_obj.device_data = device_data
    shipping_address_obj = Address.objects.filter(id=shipping_address_id).first()
    order_obj.shipping_address = shipping_address_obj
    order_obj.payment_method = nonce
    order_obj.save()
    
    request.session["shipping_address_id"] = order_obj.shipping_address.id
    return redirect("carts:checkout-confirm")

def nsnb_update(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    guest_email = request.session.get('guest_email')
    if billing_profile is None:
        email = request.POST.get('email')
        request.session['guest_email'] = email
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        print(billing_profile)
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
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    cart_items        = cartItem.objects.filter(cart=cart_obj)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    for x in cart_items:
        order_obj.items.add(x)
    order_obj.total = cart_obj.total
    order_obj.save()
    context = {
        "billing_profile": billing_profile,
        'items_list': cart_items,
        "nonce": gateway.payment_method_nonce.find(order_obj.payment_method),
        "order": order_obj,
        'cart': cart_obj,
    }
    return render(request, "carts/checkout-confirm.html", context)

def new_charge(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    if not billing_profile:
        email = request.POST.get('email')
        request.session['guest_email'] = email
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        print(billing_profile)
    charge = order_obj.charge
    order_obj.braintree_id = charge.transaction.id
    label = order_obj.new_label
    order_obj.shippo_obj = label.object_id
    order_obj.label = label.label_url
    order_obj.save()
    return redirect('carts:checkout-done')

def checkout_done(request):
    shippo.config.api_key = settings.SHIPPO_KEY
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    shippo_obj = order_obj.shippo_obj
    del request.session['cart_id']
    if not billing_profile:
        return HttpResponse({"message": "Please login or continue as a guest"}, status=401)
    context = {
        "cart": cart_obj,
        "order": order_obj,
        "shippo": shippo_obj,
        "billing_profile": billing_profile,
    }
    return render(request, "carts/checkout-done.html", context)
        

