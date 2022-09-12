from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ven.forms import BusinessForm
import json
from django.conf import settings
from donations.models import donation
from django.core.mail import send_mail

from mailchimp_marketing import Client

gateway = settings.GATEWAY_PUBLIC
mailchimp = Client()
mailchimp.set_config({
    "api_key": settings.MAILCHIMP_API_KEY,
    "server": "us7"
})

def troubleshooting(request):
    token = "tokencc_bc_9xhp78_y7z7yf_fm3db2_wjgykw_424"
    donation_obj = donation.objects.get(pk=383)
    amount = donation_obj.amount
    first_name = "Mikeisha"
    last_name = "Anderson Jones"
    email = "mikeisha@hotmail.com"
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": token,
        "custom_fields": {
            "memo": 'Donation - %s from %s %s' %(amount, first_name, last_name)
        },
        "options": {
            "submit_for_settlement": True,
        },
    })
    if result.is_success:
        donation_obj.status = 'complete'
        donation_obj.braintree_id = result.transaction.id
        donation_obj.save()
        first_name = donation_obj.first_name
        merge_fields = {
            "FNAME": str(first_name),
            "ETVAMOUNT": str(amount)
        }
        mailchimp.lists.set_list_member("bfb104d810", email, {"email_address": email, "status_if_new": "subscribed", "merge_fields": merge_fields})
        mailchimp.customerJourneys.trigger(2794, 15013, {"email_address": str(email)})
        send_mail(
            'New Donation!',
            str('A new $'+ str(amount) +' donation has been received from '+ str(donation_obj.get_full_name) +' through www.empowerthevillage.org!'),
            'etvnotifications@gmail.com',
            ['admin@empowerthevillage.org', 'chandler@eliftcreations.com', 'ayo@empowerthevillage.org'],
            #['chandler@eliftcreations.com'],
            fail_silently=True
        ) 
        print(result)
        print('successfully charged')
        data = {
            "result": str(result)
        }
        return JsonResponse(data)
    else:
        print('error')
        print(result)
        data = {
            "result": str(result)
        }
        return JsonResponse(data)
        
    
def home_page(request):
    form = BusinessForm()
    context = {
        'nomination_form': form,
        'title':'Empower The Village',
        'seo_description': 'Empower The Village, Inc. (ETV) is a data-driven nonprofit 501(c)(3) organization founded in 2018 to develop, guide and implement breakthrough, scalable strategies that empower Black people, businesses and community organizations to realize their full potential.'
    }
    return render(request, "home copy.html", context)

def about_page(request):
    context = {
    'title':'ETV | About'
    }
    return render(request, "about.html", context)

def privacy(request):
    context = {
    'title':'ETV | Privacy Policy'
    }
    return render(request, "privacy.html", context)

def terms(request):
    context = {
    'title':'ETV | Terms & Conditions'
    }
    return render(request, "terms.html", context)
    
def strategic_pillars(request):
    context = {
    'title':'ETV | Strategic Pillars'
    }
    return render(request, "strategic-pillars.html", context)

def economic_prosperity(request):
    context = {
        'title': 'ETV | Economic Prosperity & Employment',
    }
    return render(request, "prosperity.html", context)

def news(request):
    context = {
    'title':'ETV | News'
    }
    return render(request, "news.html", context)

def shop(request):
    context = {
        'title': 'ETV | Shop',
    }
    return render(request, "shop.html", context)

def robots(request):
    return render(request, "robots.txt")
