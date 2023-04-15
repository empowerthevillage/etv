from django.shortcuts import render, redirect
from .models import Walker, HomeGalleryImage, Organization, ShirtOrder, WalkerRegistrationPayment
from addresses.forms import BillingAddressForm
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string

import time
import sweetify

gateway = settings.GATEWAY

def walker_home(request):
    context = {
        'title': 'ETV 2023 Walkathon',
        'walkers': Walker.objects.all(),
        'photos': HomeGalleryImage.objects.all()
    }
    return render(request, 'walkathon_home.html', context)

def walker_detail(request, walker):
    try:
        walker_obj = Walker.objects.get(slug=walker)
        print(walker_obj)
        context = {
            'title': 'Support %s' %(walker_obj),
            'walker': walker_obj
        }
        return render(request, 'walker_detail.html', context)
    except:
        return redirect('/walkathon/')
    
def walker_registration(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        data = request.POST
        files = request.FILES
        nonce_id = data['nonce']
        first_name = data['walker_first_name']
        last_name = data['walker_last_name']
        email = data['email']
        total = data['order-total']
        result = gateway.transaction.sale({
            "amount": total,
            "payment_method_nonce": nonce_id,
            "customer": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            },
            "custom_fields": {
                "memo": 'Power Walk Registration - %s %s' %(first_name, last_name)
            },
            "options": {
                "submit_for_settlement": True,
            },
        })
        if result.is_success:
            try:
                if data['organization'] != '':
                    org = Organization.objects.get(title=data['organization'])
                else:
                    org = None
            except:
                org = None
            walker_obj = Walker()
            walker_obj.first_name = first_name
            walker_obj.last_name = last_name
            walker_obj.title = '%s %s' %(first_name, last_name)
            walker_obj.email = email
            walker_obj.phone = data['phone']
            walker_obj.organization = org
            walker_obj.emergency_contact_name = data['emergency-contact-name']
            walker_obj.emergency_contact_phone = data['emergency-contact-phone']
            walker_obj.address_line_1 = data['address_line_1']
            walker_obj.address_line_2 = data['address_line_2']
            walker_obj.city = data['city']
            walker_obj.state = data['state']
            walker_obj.zip = data['zip']
            try:
                walker_obj.image = files['image']
            except:
                pass
            try:
                walker_obj.donation_goal = float(request.POST['fundraising-goal'].replace(",", ""))
            except:
                pass
            walker_obj.save()
            payment = WalkerRegistrationPayment()
            payment.braintree_id = result.transaction.id
            payment.complete = True
            payment.amount = data['order-total']
            payment.walker = walker_obj
            payment.save()
            try:
                if data['shirt-boolean'] == 'on':
                    shirt_obj = ShirtOrder()
                    shirt_obj.braintree_id = result.transaction.id
                    shirt_obj.complete = True
                    shirt_obj.amount = 20.00
                    shirt_obj.shirt_size = data['shirt-size']
                    shirt_obj.walker = walker_obj
                    shirt_obj.save()
                    shirt_ordered = True
                else:
                    shirt_ordered = False
                    shirt_obj = None
            except:
                shirt_ordered = False
                shirt_obj = None
            data = {
                'status': 'success',
                'html': render_to_string('registration-details.html', context={'walker': walker_obj,
                    'shirt_ordered': shirt_ordered,
                    'shirt': shirt_obj,
                    'payment_method': result.transaction.credit_card_details,
                    'total': total,
                })
            }
            return JsonResponse(data)
        else:
            data = {
                'status': 'error',
                'message': 'There was an issue processing your payment method. Please verify your card details and try again'
            }
            return JsonResponse(data)
    else:
        tokenization_key = settings.BRAINTREE_TOKENIZATION_KEY
        orgs = Organization.objects.all()
        context = {
            'tokenization_key': tokenization_key,
            'mailing_form': BillingAddressForm(),
            'orgs': orgs,
        }
        return render(request, 'registration_form.html', context)
    
def org_registration(request):
    if request.method == 'POST':
        org, created = Organization.objects.get_or_create(title = request.POST['organization'])
        if created == True:
            org.captain_first_name = request.POST['first_name']
            org.captain_last_name = request.POST['last_name']
            org.email = request.POST['email']
            try:
                org.donation_goal = float(request.POST['fundraising-goal'].replace(",", ""))
            except:
                pass
            if request.POST['image'] != '':
                org.image = request.FILES['image']
            org.save()
            context = {
                'new_org_popup': True,
            }
            return render(request, 'org-registration.html', context)
        else:
            context = {
                'already_registered_popup': True
            }
            return render(request, 'org-registration.html', context)
    else:
        return render(request, 'org-registration.html')