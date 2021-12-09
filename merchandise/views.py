from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *
from django.http import Http404, JsonResponse
from carts.models import Cart, cartItem
from django.db.models import Q

import django_filters
import sweetify

def ProductList(request):
    object_list = newProduct.objects.all()
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_items = cartItem.objects.filter(cart=cart_obj)
    context = {
        'cart': cart_obj,
        'cart_items': cart_items,
        'title': 'ETV | Shop',
        'object_list': object_list
    }
    return render(request, 'new_list.html', context)

def AddToCart(request):
    color = request.GET['color']
    id = request.GET['id']
    size = request.GET['size']
    order_sku = '%s-%s-%s' %(id, size, color)
    inv_item = newInventory.objects.filter(sku=order_sku).first()
    (invItem) = inv_item
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_item = cartItem.objects.filter(item=invItem, cart=cart_obj).first()
    if cart_item is not None:
        cart_item.quantity += 1
        print(cart_item.quantity)
        cart_item.save()
    else:
        obj = cartItem()
        obj.cart = cart_obj
        obj.item = invItem
        obj.quantity = 1
        obj.product = invItem.product
        obj.save()
    
    return redirect('merchandise:list')

def RemoveFromCart(request):
    color = request.GET['color']
    id = request.GET['id']
    size = request.GET['size']
    order_sku = '%s-%s-%s' %(id, size, color)

    if order_sku is not None:
        inventoryItem = newInventory.objects.filter(sku=order_sku).first()
        (invItem) = inventoryItem
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        (cart_items) = cart_obj.items.filter(sku=invItem).first()
        if cart_items is not None:
            item_obj = cart_items
            currentQuantity = item_obj.quantity
            item_obj.quantity = currentQuantity - 1
            item_obj.save()
        else:
            errorData = str('Nothing to remove!')
                
    return redirect('merchandise:list')

def cart_update(request):
    type = request.POST.get('type')
    size = request.POST.get('size')
    color = request.POST.get('color')
    if type is not None:
        
        try:
            item_obj = item.objects.get(type=type, color=color, size=size)
        
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