from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe

from datetime import datetime, timedelta

from accounts.models import *
from addresses.models import *
from analytics.models import *
from bfchallenge.models import *
from billing.models import *
from carts.models import *
from content.models import *
from donations.models import *
from donors.models import *
from events.models import *
from merchandise.models import *
from orders.models import *
from vbp.models import *
from ven.models import *

from etv.mixins import NextUrlMixin, RequestFormAttachMixin
from accounts.models import GuestEmail
from accounts.signals import user_logged_in

import datetime
import pandas as pd
from django.shortcuts import render, redirect
import sweetify

User = get_user_model()
gateway = settings.GATEWAY

def updateDonors(request):
    donors = Donor.objects.all()
    for x in donors:
        print(x.get_total)
        x.total = x.get_total
        x.save()
    return HttpResponse('success')

def DashboardHome(request):
    #Accounts
    users = MyUser.objects.all()
    teams = Team.objects.all()
    bfc_partiipants = Participant.objects.all()

    #Addresses
    addresses = Address.objects.all()

    #BFChallenge
    bingo_cards = bingo_card.objects.all()
    user_bingo_cards = user_bingo_card.objects.all()
    user_bingo_forms = user_bingo_form.objects.all()
    rss_transactions = readysetshop_transaction.objects.all()
    vbp_nomination = nomination.objects.all()

    #Billing
    billing_profiles = BillingProfile.objects.all()

    #Carts
    shopping_carts = Cart.objects.all()
    ticket_carts = TicketCart.objects.all()

    #Content
    contact_requests = contact_submission.objects.all()

    #Donations
    donations = donation.objects.all()
    tags = tag.objects.all()
    donation_events = donation_event.objects.all()
    donors = Donor.objects.all()

    top_donors = donors.order_by('-total')[:5]
    
    d = datetime.datetime.now() - timedelta(days=30)
    date_range = pd.date_range(start=d, end=datetime.datetime.now())
    
    latest_donations = donations.filter(status="complete").filter(updated__range=[str(d), str(datetime.datetime.now())])
    last_5_donations = donations.filter(status="complete").order_by('-updated')[:5]

    #Events
    events = Event.objects.all()

    #Ticketing
    ticket_types = TicketType.objects.all()
    tickets = SingleTicket.objects.all()

    latest_tickets = tickets.filter(updated__range=[str(d), str(datetime.datetime.now())])
    last_5_tickets = tickets.order_by('-updated')[:5]

    #Orders
    orders = Order.objects.all()

    all_dates = []
    all_donation_dates = []
    all_donation_amounts = []
    donation_dates = []
    all_ticket_dates = []
    all_ticket_amounts = []
    ticket_dates = []
    donation_amounts = []
    ticket_amounts = []

    for i in date_range:
        all_dates.append('%s-%s-%s' %(i.year, i.strftime("%m"), i.strftime("%d")))
        all_donation_dates.append('%s-%s-%s' %(i.year, i.strftime("%m"), i.strftime("%d")))
        all_donation_amounts.append(0)
        all_ticket_dates.append('%s-%s-%s' %(i.year, i.strftime("%m"), i.strftime("%d")))
        all_ticket_amounts.append(0)
        
    for x in latest_donations:
        year = x.updated.year
        month = x.updated.strftime("%m")
        day = x.updated.strftime("%d")
        all_donation_dates.append('%s-%s-%s' %(year, month, day))
        all_donation_amounts.append(int(x.amount))

    donation_df = pd.DataFrame({'Date': all_donation_dates, 'Amount': all_donation_amounts})
    grouped_donations = donation_df.groupby('Date').sum().to_dict()["Amount"]

    for x in grouped_donations:
        donation_dates.append(x)
        donation_amounts.append(grouped_donations[x])

    for x in latest_tickets:
        year = x.updated.year
        month = x.updated.strftime("%m")
        day = x.updated.strftime("%d")
        all_ticket_dates.append('%s-%s-%s' %(year, month, day))
        all_ticket_amounts.append(int(x.type.price))
    
    ticket_df = pd.DataFrame({'Date': all_ticket_dates, 'Amount': all_ticket_amounts})
    grouped_tickets = ticket_df.groupby('Date').sum().to_dict()["Amount"]

    for x in grouped_tickets:
        ticket_dates.append(x)
        ticket_amounts.append(grouped_tickets[x])

    context = {
        "donation_data": grouped_donations,
        "ticket_data": grouped_tickets,
        "dates": all_dates,
        "donation_dates": donation_dates,
        "ticket_dates": ticket_dates,
        "donation_amounts": donation_amounts,
        "ticket_amounts": ticket_amounts,
        "min": d,
        "now": datetime.datetime.now(),
        "last_5_donations": last_5_donations,
        "last_5_tickets": last_5_tickets,
        "tickets": tickets,
        "orders": orders,
        "top_donors": top_donors
    }

    return render(request,'dashboard-home.html', context)