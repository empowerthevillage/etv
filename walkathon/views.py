from django.shortcuts import render, redirect
from .models import Walker, HomeGalleryImage, Organization, ShirtOrder, WalkerRegistrationPayment, Sponsorship, WalkerDonation, OrgDonation, WalkerPledgePayment
from addresses.forms import BillingAddressForm
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string

import time
import sweetify
from django.core.mail import send_mail

from mailchimp_marketing import Client

mailchimp = Client()
mailchimp.set_config({
    "api_key": settings.MAILCHIMP_API_KEY,
    "server": "us7"
})

gateway = settings.GATEWAY

def walker_home(request):
    individuals = Walker.objects.all()
    orgs = Organization.objects.all()
    dropdown_list = []
    for x in individuals:
        dropdown_list.append(x)
    for x in orgs:
        paid_count = Walker.objects.filter(organization=x)
        if len(paid_count) > 0:
            dropdown_list.append(x)
    context = {
        'title': 'ETV 2023 Power Walk',
        'photos': HomeGalleryImage.objects.all(),
        'dropdown_list': sorted(dropdown_list, key=lambda x: x.title)
    }
    return render(request, 'walkathon_home.html', context)

def walker_detail(request, walker):
    try:
        try:
            walker_obj = Walker.objects.get(slug=walker)
            walker_type = 'individual'
            walker_list = ''
            donation_list = WalkerDonation.objects.filter(walker=walker_obj)
        except:
            walker_obj = Organization.objects.get(slug=walker)
            walker_list = Walker.objects.filter(organization=walker_obj)
            walker_type = 'org'
            donation_list = OrgDonation.objects.filter(organization=walker_obj)
        context = {
            'title': 'Support %s' %(walker_obj),
            'walker': walker_obj,
            'walker_type': walker_type,
            'walker_list': walker_list,
            'donation_list': donation_list,
        }
        return render(request, 'walker_detail.html', context)
    except:
       return redirect('/power-walk-2023/')

def org_walker_detail(request, org, walker):
    walker_obj = Walker.objects.get(slug=walker)
    walker_type = 'individual'
    walker_list = ''
    donation_list = WalkerDonation.objects.filter(walker=walker_obj).filter(complete=True)
    context = {
        'title': 'Support %s' %(walker_obj),
        'walker': walker_obj,
        'walker_type': walker_type,
        'walker_list': walker_list,
        'donation_list': donation_list,
        'org_walker': True,
    }
    return render(request, 'walker_detail.html', context)

def walker_registration(request):
    if request.method == 'POST':
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
            send_mail(
                'New Power Walk Registration!',
                str('A new $%s power walk registration has been processed for %s %s through www.empowerthevillage.org!' %(total, first_name, last_name)),
                'etvnotifications@gmail.com',
                ['admin@empowerthevillage.org', 'chandler@eliftcreations.com', 'ayo@empowerthevillage.org'],
                #['chandler@eliftcreations.com'],
                fail_silently=True
            )
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
            if data['virtual-selection'] == 'virtually':
                walker_obj.virtual = True
            elif data['virtual-selection'] == 'in-person':
                walker_obj.virtual = False
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
                if data['pledge'] == 'true':
                    pledge_obj = WalkerPledgePayment()
                    pledge_obj.braintree_id = result.transaction.id
                    pledge_obj.complete = True
                    pledge_obj.amount = request.POST['fundraising-goal']
                    pledge_obj.walker = walker_obj
                    pledge_obj.save()
                    pledge_paid = True
                else:
                    pledge_paid = False
                    pledge_obj = None
            except:
                pledge_paid = False
                pledge_obj = None
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
                    'pledge_paid': pledge_paid,
                    'shirt': shirt_obj,
                    'pledge': pledge_obj,
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
            orgs = Organization.objects.exclude(pk=org.pk)
            tokenization_key = settings.BRAINTREE_TOKENIZATION_KEY
            context = {
                'new_org_popup': True,
                'org_created': org,
                'orgs': orgs,
                'tokenization_key': tokenization_key,
                'mailing_form': BillingAddressForm(),
            }
            return render(request, 'registration_form.html', context)
        else:
            context = {
                'already_registered_popup': True
            }
            return render(request, 'org-registration.html', context)
    else:
        
        return render(request, 'org-registration.html')
    
def sponsor(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        nonce_id = data['nonce']
        first_name = data['first_name']
        last_name = data['last_name']
        organization = data['organization']
        email = data['email']
        total = data['sponsorship-level']
        spons_obj = Sponsorship()
        result = gateway.transaction.sale({
            "amount": total,
            "payment_method_nonce": nonce_id,
            "customer": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            },
            "custom_fields": {
                "memo": 'Power Walk Sponsorship - %s %s' %(first_name, last_name)
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
                'New Power Walk Sponsorship!',
                str('A new $%s sponsorship has been received from %s %s through www.empowerthevillage.org!' %(total, spons_obj.first_name, spons_obj.last_name)),
                'etvnotifications@gmail.com',
                ['admin@empowerthevillage.org', 'chandler@eliftcreations.com', 'ayo@empowerthevillage.org'],
                #['chandler@eliftcreations.com'],
                fail_silently=True
            )
            spons_obj.first_name = first_name
            spons_obj.last_name = last_name
            spons_obj.email = email
            spons_obj.phone = data['phone']
            spons_obj.organization = organization
            spons_obj.address_line_1 = data['address_line_1']
            spons_obj.address_line_2 = data['address_line_2']
            spons_obj.city = data['city']
            spons_obj.state = data['state']
            spons_obj.zip = data['zip']
            spons_obj.braintree_id = result.transaction.id
            spons_obj.complete = True
            spons_obj.amount = total
            try:
                spons_obj.image = files['image']
            except:
                pass
            spons_obj.save()
            data = {
                    'status': 'success',
                    'html': render_to_string('sponsor-success.html', context={'sponsorship': spons_obj,
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
        context = {
            'tokenization_key': tokenization_key,
            'mailing_form': BillingAddressForm(),
        }
        return render(request, 'sponsor-walk.html', context)
    
def sponsor_walker(request):
    if request.method == 'POST':
        print(request.POST)
        request.session['selected-amount'] = request.POST['support-amount']
        request.session['walker'] = request.POST['walker-pk']
        request.session['walker_type'] = request.POST['walker-type']
        data = {
            'status': 'success'
        }
        return JsonResponse(data)

def walker_donation_form(request):
    tokenization_key = settings.BRAINTREE_TOKENIZATION_KEY
    walker_type = request.session['walker_type']
    walker_id = request.session['walker']
    amount = request.session['selected-amount']
    if walker_type == 'individual':
        walker = Walker.objects.get(pk=walker_id)
    elif walker_type == 'org':
        walker = Organization.objects.get(pk=walker_id)
    context = {
        'tokenization_key': tokenization_key,
        'mailing_form': BillingAddressForm(),
        'walker': walker,
        'amount': amount,
        'walker_type': walker_type,
    }
    return render(request, 'support-walker-unique.html', context)
    
def process_walker_donation(request):
    if request.method == 'POST':
        data = request.POST
        nonce_id = data['nonce']
        first_name = data['first_name']
        last_name = data['last_name']
        walker_type = data['walker_type']
        walker_id = data['walker_pk']
        if walker_type == 'individual':
            walker = Walker.objects.get(pk=walker_id)
            spons_obj = WalkerDonation()
            spons_obj.walker = walker
        elif walker_type == 'org':
            walker = Organization.objects.get(pk=walker_id)
            spons_obj = OrgDonation()
            spons_obj.organization = walker
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
                "memo": '$%s Power Walker Donation for %s from %s %s' %(total, walker, first_name, last_name)
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
                'New Power Walk Donation!',
                str('A new $%s Power Walk donation for %s has been received from %s %s through www.empowerthevillage.org!' %(total, walker, first_name, last_name)),
                'etvnotifications@gmail.com',
                ['admin@empowerthevillage.org', 'chandler@eliftcreations.com', 'ayo@empowerthevillage.org'],
                #['chandler@eliftcreations.com'],
                fail_silently=True
            )
            
            spons_obj.first_name = first_name
            spons_obj.last_name = last_name
            spons_obj.email = email
            spons_obj.phone = data['phone']
            spons_obj.address_line_1 = data['address_line_1']
            spons_obj.address_line_2 = data['address_line_2']
            spons_obj.city = data['city']
            spons_obj.state = data['state']
            spons_obj.zip = data['zip']
            spons_obj.message = data['message']
            spons_obj.braintree_id = result.transaction.id
            spons_obj.complete = True
            spons_obj.amount = total
            spons_obj.save()
            data = {
                    'status': 'success',
                    'html': render_to_string('walker-donation-success.html', context={'donation': spons_obj,
                        'payment_method': result.transaction.credit_card_details,
                        'walker_type': walker_type,
                    })
            }
            return JsonResponse(data)
        else:
            data = {
                'status': 'error',
                'message': 'There was an issue processing your payment method. Please verify your card details and try again'
            }
            return JsonResponse(data)