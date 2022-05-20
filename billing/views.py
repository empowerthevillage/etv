from telnetlib import STATUS
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.transaction import atomic, non_atomic_requests
from django.http.response import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import BraintreeTransaction, Disbursement
from donations.models import DonationManager, donation
from events.models import CompleteDonation, SingleTicket
from orders.models import Order, LOAPresalePurchase

import braintree
import json

gateway = settings.GATEWAY

@csrf_exempt
@require_POST
def braintree_disbursement(request):
    signature = str(request.POST['bt_signature'])
    payload = str(request.POST['bt_payload'])
    webhook_notification = gateway.webhook_notification.parse(signature, payload)
    dict = (webhook_notification.subject['disbursement'])
    disbursement_id = dict['id']
    transaction_ids = dict['transaction_ids']
    date = dict['disbursement_date']
    obj = Disbursement()
    obj.disbursement_date = date
    obj.disbursement_id = disbursement_id
    obj.transactions = transaction_ids
    obj.save()

    return HttpResponse(status=200)

def disbursement_test(request):
    sample_notification = gateway.webhook_testing.sample_notification(braintree.WebhookNotification.Kind.Disbursement, "rando")
    webhook_notification = gateway.webhook_notification.parse(
        sample_notification['bt_signature'],
        sample_notification['bt_payload']
    )
    dict = (webhook_notification.subject['disbursement'])
    disbursement_id = dict['id']
    transaction_ids = dict['transaction_ids']
    date = dict['disbursement_date']
    amount = dict['amount']
    obj = Disbursement()
    obj.disbursement_date = date
    obj.disbursement_id = disbursement_id
    obj.transactions = transaction_ids
    obj.amount = amount
    return HttpResponse(status=200)

def populate_transactions(request):
    donations = donation.objects.all()
    event_donations = CompleteDonation.objects.all()
    tickets = SingleTicket.objects.all()
    orders = Order.objects.all()
    loa_purchases = LOAPresalePurchase.objects.all()
    for x in donations:
        if x.braintree_id is not None:
            obj = BraintreeTransaction()
            obj.braintree_id = x.braintree_id
            obj.item = 'Donation'
            obj.purchaser = '%s %s' %(x.first_name, x.last_name)
            obj.amount = x.amount
            obj.url = '/dashboard/donations/donation-list/view/%s' %(x.pk)
            obj.save()
    for x in event_donations:
        if x.braintree_id is not None:
            obj = BraintreeTransaction()
            obj.braintree_id = x.braintree_id
            obj.item = 'Event Donation - %s' %(x.event)
            obj.purchaser = '%s %s' %(x.first_name, x.last_name)
            obj.amount = x.amount
            obj.url = '/dashboard/donations/CompleteDonation-list/view/%s' %(x.pk)
            obj.save()
    for x in tickets:
        obj = BraintreeTransaction()
        obj.braintree_id = x.braintree_id
        obj.item = 'Ticket - %s' %(x.type)
        obj.purchaser = '%s %s' %(x.first_name, x.last_name)
        obj.amount = x.purchase_price
        obj.url = '/dashboard/orders/SingleTicket-list/view/%s' %(x.pk)
        obj.save()
    for x in orders:
        if x.braintree_id is not None:
            obj = BraintreeTransaction()
            obj.braintree_id = x.braintree_id
            obj.item = 'Merchandise Order'
            obj.purchaser = '%s %s' %(x.first_name, x.last_name)
            obj.amount = x.total
            obj.url = ""
            obj.save()
    for x in loa_purchases:
        if x.braintree_id is not None:
            obj = BraintreeTransaction()
            obj.braintree_id = x.braintree_id
            obj.item = 'Art Gallery Purchase'
            obj.purchaser = '%s %s' %(x.first_name, x.last_name)
            obj.url = '/dashboard/orders/LOAPresalePurchase-list/view/%s' %(x.pk)
            obj.amount = x.total
            obj.save()
    return HttpResponse(status=200)
    
