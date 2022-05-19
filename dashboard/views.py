import re
import django
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.db import connection
from django.forms import ModelForm
from django.http import HttpResponse
from django.views.generic.edit import FormMixin
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
from etv.utils import field_type_generator
from events.models import *
from merchandise.models import *
from orders.models import *
from vbp.models import *
from ven.models import *

from .models import *
from .forms import *

from etv.mixins import NextUrlMixin, RequestFormAttachMixin
from accounts.models import GuestEmail
from accounts.signals import user_logged_in

import datetime
import pandas as pd
from django.shortcuts import render, redirect
import sweetify
import csv

User = get_user_model()
gateway = settings.GATEWAY_PUBLIC

def updateDonors(request):
    donors = Donor.objects.all()
    for x in donors:
        print(x.get_total)
        x.total = x.get_total
        x.save()
    return HttpResponse('success')

@csrf_exempt
def braintree_accounting(request):
    print(request.POST)
    Disbursement.objects.create(notification='notification not too long')
    if request.method == 'POST':
        webhook_notification = gateway.webhook_notification.parse(str(request.form['bt_signature']), request.form['bt_payload'])
        Disbursement.objects.create(notification=webhook_notification)
        Disbursement.objects.create(notification='notification not too long')
        context={
            "webhook_notification": webhook_notification
        }
        return render(request, 'braintree-dash.html', context, status=200)
    else:
        return HttpResponse('no webhook received')

def DashboardHome(request):
    #Donations
    donations = donation.objects.all()
    donors = Donor.objects.all()

    top_donors = donors.order_by('-total')[:5]
    
    d = datetime.datetime.now() - timedelta(days=30)
    date_range = pd.date_range(start=d, end=datetime.datetime.now())
    
    latest_donations = donations.filter(status="complete").filter(updated__range=[str(d), str(datetime.datetime.now())])
    last_5_donations = donations.filter(status="complete").order_by('-updated')[:5]

    tickets = SingleTicket.objects.all()

    latest_tickets = tickets.filter(updated__range=[str(d), str(datetime.datetime.now())])
    last_5_tickets = tickets.order_by('-created')[:5]

    #Orders
    orders = Order.objects.all()

    app_list = dashboardModel.objects.all().order_by('category', 'model_name')

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
        year = x.created.year
        month = x.created.strftime("%m")
        day = x.created.strftime("%d")
        all_donation_dates.append('%s-%s-%s' %(year, month, day))
        all_donation_amounts.append(int(x.amount))

    donation_df = pd.DataFrame({'Date': all_donation_dates, 'Amount': all_donation_amounts})
    grouped_donations = donation_df.groupby('Date').sum().to_dict()["Amount"]

    for x in grouped_donations:
        donation_dates.append(x)
        donation_amounts.append(grouped_donations[x])

    for x in latest_tickets:
        year = x.created.year
        month = x.created.strftime("%m")
        day = x.created.strftime("%d")
        all_ticket_dates.append('%s-%s-%s' %(year, month, day))
        all_ticket_amounts.append(int(x.type.price))
    
    ticket_df = pd.DataFrame({'Date': all_ticket_dates, 'Amount': all_ticket_amounts})
    grouped_tickets = ticket_df.groupby('Date').sum().to_dict()["Amount"]

    for x in grouped_tickets:
        ticket_dates.append(x)
        ticket_amounts.append(grouped_tickets[x])

    context = {
        "app_list": app_list,
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

def appHome(request, category):
    app_list = dashboardModel.objects.all().order_by('category', 'model_name')
    model_list = dashboardModel.objects.filter(category=str(category))
    context = {
        "category": category,
        "models": model_list,
        "app_list": app_list,
    }
    return render(request, 'app-home.html', context)

def modelHome(request, category, model):
    app_list = dashboardModel.objects.all().order_by('category', 'model_name')
    model_obj = dashboardModel.objects.filter(model_name=str(model)).first()
    model = django.apps.apps.get_model(str(model_obj.app_name), str(model))
    filtered_objs = model.objects.filter_objs()
    objs = model.objects.all()
    fields = model.objects.dashboard_get_fields()
    field_list = []
    field_name_list = ['pk']
    field_pairs = []
    data_list = []

    ticket_type_list = {}
    event_list ={}
    art_list ={}
    ticket_pks = TicketType.objects.all()
    for x in ticket_pks:
        ticket_type_list.update({str(x.pk):str(x.title)})
    event_pks = Event.objects.all()
    for x in event_pks:
        event_list.update({str(x.pk):str(x.title)})
    art_pks = GalleryItem.objects.all()
    for x in art_pks:
        art_list.update({str(x.pk):str(x.artist)})

    for x in fields:
        item = model._meta.get_field(str(x["field"]))
        type = x["type"]
        field_list.append(item)
        field_name_list.append(item.name)
        field_pairs.append({"field": item, "type": type, "verbose": item.verbose_name})
    
    data = model.objects.filter_objs().values_list(*field_name_list, named=True)
    p = Paginator(data, model.objects.dashboard_display_qty())

    context = {
        "dashboardModel": model_obj,
        "model": model,
        "objs": objs,
        "fields": field_pairs,
        "field_names": field_name_list,
        "data": data,
        "p": p,
        "app_list": app_list,
        "ticketTypes": json.dumps(ticket_type_list),
        "eventTypes": json.dumps(event_list),
        "artists": json.dumps(art_list),
    }
    return render(request, 'model-home.html', context)

def objectChange(request, category, model, pk):

    app_list = dashboardModel.objects.all().order_by('category', 'model_name')
    model_obj = dashboardModel.objects.filter(model_name=str(model)).first()
    model = django.apps.apps.get_model(str(model_obj.app_name), str(model))
    obj = model.objects.filter(pk=pk).first()
    form = None
    form_pairs = [
        {'model':'contact_submission','form':ContactForm(instance=obj)},
        {'model':'donation','form':DonationForm(instance=obj)},
        {'model':'Donor','form':DonorForm(instance=obj)},
        {'model':'Event','form':EventForm(instance=obj)},
        {'model':'Ad','form':AdForm(instance=obj)},
        {'model':'CompleteDonation','form':EventDonationForm(instance=obj)},
        {'model':'SingleTicket','form':TicketForm(instance=obj)},
        {'model':'TicketType','form':TicketTypeForm(instance=obj)},
        {'model':'Nomination','form':VenBusinessForm(instance=obj)},
        {'model':'FamilyNomination','form':VenFamilyForm(instance=obj)},
        {'model':'vbp_book','form':VBPBookForm(instance=obj)},
    ]
    
    for x in form_pairs:
        if model_obj.model_name == x['model']:
            form = x['form']
    
    fields = model._meta.get_fields()
    fields_formatted = []
    for x in fields:
        field_type = field_type_generator(x)
        if field_type == 'choice':
            choices = x.choices
        else:
            choices = ''
        try:
            formfield = x.formfield()
            widget_html = formfield.widget.render
        except:
            formfield = 'manytomany'
            widget_html = ''
        try:
            value = x.value_from_object(obj)
        except:
            value = 'here'
        fields_formatted.append({"field": x, "type": field_type, "value": value, "formfield": formfield, "widget_html": widget_html, "choices": choices,})
        
    context = {
        "model": model,
        "dashboardModel": model_obj,
        "obj": obj,
        "fields": fields,
        "fields_formatted": fields_formatted,
        "app_list": app_list,
        "form": form
    }
    return render(request, 'obj-change.html', context)

def objectView(request, category, model, pk):
    app_list = dashboardModel.objects.all().order_by('category', 'model_name')
    model_obj = dashboardModel.objects.filter(model_name=str(model)).first()
    model = django.apps.apps.get_model(str(model_obj.app_name), str(model))
    obj = model.objects.filter(pk=pk).first()
    fields = model.objects.dashboard_get_view_fields()
    field_pairs = []
    for x in fields:
        item = model._meta.get_field(str(x["field"]))
        type = x["type"]
        try:
            value = item.value_from_object(obj)
        except:
            value = 'No Value'
        field_pairs.append({"field": item, "type": type, "verbose": item.verbose_name, "value": value})
        if type == 'braintree_transaction':
            try:
                transaction = gateway.transaction.find(str(value))
                if transaction.payment_instrument_type == 'credit_card':
                    field_pairs.append({"field": "Payment Method", "type": 'card-detail', "verbose": "Payment Method", "card_logo_url": transaction.credit_card_details.image_url, "value": "%s ending in %s" %(transaction.credit_card_details.card_type, transaction.credit_card_details.last_4)})
                elif transaction.payment_instrument_type == 'paypal_account':
                    field_pairs.append({"field": "Payment Method", "type": 'plain', "verbose": "Payment Method", "value": "PayPal"})
                else:
                    field_pairs.append({"field": "Payment Method", "type": 'plain', "verbose": "Payment Method", "value": "%s" %(transaction.payment_instrument_type)})
            except:
                pass
    context = {
        "model": model,
        "dashboardModel": model_obj,
        "pairs": field_pairs,
        "obj": obj,
        "app_list": app_list,
    }
    return render(request, 'obj-view.html', context)

def download_csv(request):
        if not request.user.is_staff:
            raise PermissionDenied
        data = request.POST
        model = data.model
        print(model)
        #opts = data.model
        #opts = queryset.model._meta
        #model = queryset.model
        #response = HttpResponse(mimetype='text/csv')
        # force download.
        #response['Content-Disposition'] = 'attachment;filename=export.csv'
        # the csv writer
        #writer = csv.writer(response)
        #field_names = [field.name for field in opts.fields]
        # Write a first row with header information
        #writer.writerow(field_names)
        # Write data rows
        #for obj in queryset:
        #    writer.writerow([getattr(obj, field) for field in field_names])
        #return response

def delete_obj(request):
    if request.user.is_admin:
        dashmodel = request.POST.get('dashmodel')
        pk = request.POST.get('pk')
        model_obj = dashboardModel.objects.filter(model_name=dashmodel).first()
        model = django.apps.apps.get_model(str(model_obj.app_name), str(model_obj.model_name))
 
        obj = model.objects.get(pk=pk)
        obj.delete()
        data = {
            'status': 'success'
        }
        return JsonResponse(data)

def save_obj(request):
    if request.user.is_admin:
        model = request.POST.get('model')
        pk = request.POST.get('pk')
        if model == 'contact_submission':
            instance = contact_submission.objects.get(pk=pk)
            form = ContactForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Contact%sUs/contact_submission-list/view/%s' %('%20', pk)
        elif model == 'donation':
            instance = donation.objects.get(pk=pk)
            form = DonationForm(request.POST, instance=instance)
            redirect_url = '/dashboard/donations/donation-list/view/%s' %(pk)
        elif model == 'Donor':
            instance = Donor.objects.get(pk=pk)
            form = DonorForm(request.POST, instance=instance)
            redirect_url = '/dashboard/donations/Donor-list/view/%s' %(pk)
        elif model == 'Event':
            instance = Event.objects.get(pk=pk)
            form = EventForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Events/Event-list/view/%s' %(pk)
        elif model == 'Ad':
            instance = Ad(pk=pk)
            form = AdForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Events/Ad-list/view/%s' %(pk)
        elif model == 'CompleteDonation':
            instance = CompleteDonation(pk=pk)
            form = EventDonationForm(request.POST, instance=instance)
            redirect_url = '/dashboard/donations/CompleteDonation-list/view/%s' %(pk)
        elif model == 'SingleTicket':
            instance = SingleTicket.objects.get(pk=pk)
            form = TicketForm(request.POST, instance=instance)
            redirect_url = '/dashboard/orders/SingleTicket-list/view/%s' %(pk)
        elif model == 'TicketType':
            instance = TicketType.objects.get(pk=pk)
            form = TicketTypeForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Events/TicketType-list/view/%s' %(pk)
        elif model == 'Nomination':
            instance = Nomination.objects.get(pk=pk)
            prev_counselor = instance.counselor
            form = VenBusinessForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Village%sEmpowerment%sNetwork/Nomination-list/view/%s' %('%20','%20', pk)
        elif model == 'FamilyNomination':
            instance = FamilyNomination.objects.get(pk=pk)
            form = VenFamilyForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Village%sEmpowerment%sNetwork/FamilyNomination-list/view/%s' %('%20','%20', pk)
        elif model == 'vbp_book':
            instance = vbp_book.objects.get(pk=pk)
            form = VBPBookForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Village%sBlack%sPages/vbp_book-list/view/%s' %('%20','%20',pk)
        form.save()
        if model == 'Nomination':
            if prev_counselor != instance.counselor:
                subject = "Congratulations! You've Matched With A Village Empowerment Network Counselor!"
                from_email = 'etvnotifications@gmail.com'
                content = render_to_string('counselor-assignment.html',
                {
                    'counselor':instance.counselor,
                    'counsel_link':'https://empowerthevillage.org/village-empowerment-network/schedule/%s' %(instance.ven_id)
                })
                plain_text = 'View email in browser'
                send_mail(subject, plain_text, from_email, [str(instance.nominator_email)], html_message=content)
            else:
                print('no new counselor')
        sweetify.success(request, 'Update Successful!')
        return redirect(redirect_url)

def objectNew(request, category, model):

    app_list = dashboardModel.objects.all().order_by('category', 'model_name')
    model_obj = dashboardModel.objects.filter(model_name=str(model)).first()
    model = django.apps.apps.get_model(str(model_obj.app_name), str(model))

    form = None
    form_pairs = [
        {'model':'contact_submission','form':ContactForm()},
        {'model':'donation','form':DonationForm()},
        {'model':'Donor','form':DonorForm()},
        {'model':'Event','form':EventForm()},
        {'model':'Ad','form':AdForm()},
        {'model':'CompleteDonation','form':EventDonationForm()},
        {'model':'SingleTicket','form':TicketForm()},
        {'model':'TicketType','form':TicketTypeForm()},
        {'model':'Nomination','form':VenBusinessForm()},
        {'model':'FamilyNomination','form':VenFamilyForm()},
        {'model':'vbp_book','form':VBPBookForm()},
    ]
    
    for x in form_pairs:
        if model_obj.model_name == x['model']:
            form = x['form']
    
    fields = model._meta.get_fields()
    fields_formatted = []
    for x in fields:
        field_type = field_type_generator(x)
        if field_type == 'choice':
            choices = x.choices
        else:
            choices = ''
        try:
            formfield = x.formfield()
            widget_html = formfield.widget.render
        except:
            formfield = 'manytomany'
            widget_html = ''
  
        fields_formatted.append({"field": x, "type": field_type, "formfield": formfield, "widget_html": widget_html, "choices": choices,})
        
    context = {
        "model": model,
        "dashboardModel": model_obj,
        "fields": fields,
        "fields_formatted": fields_formatted,
        "app_list": app_list,
        "form": form
    }
    return render(request, 'obj-new.html', context)

def new_obj(request):
    if request.user.is_admin:
        model = request.POST.get('model')
        if model == 'contact_submission':
            instance = contact_submission()
            form = ContactForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Contact%sUs/contact_submission-list/' %('%20')
        elif model == 'donation':
            instance = donation()
            form = DonationForm(request.POST, instance=instance)
            redirect_url = '/dashboard/donations/donation-list/'
        elif model == 'Donor':
            instance = Donor()
            form = DonorForm(request.POST, instance=instance)
            redirect_url = '/dashboard/donations/Donor-list/'
        elif model == 'Event':
            instance = Event()
            form = EventForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Events/Event-list/'
        elif model == 'Ad':
            instance = Ad()
            form = AdForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Events/Ad-list/'
        elif model == 'CompleteDonation':
            instance = CompleteDonation()
            form = EventDonationForm(request.POST, instance=instance)
            redirect_url = '/dashboard/donations/CompleteDonation-list/'
        elif model == 'SingleTicket':
            instance = SingleTicket()
            form = TicketForm(request.POST, instance=instance)
            redirect_url = '/dashboard/order/SingleTicket-list/'
        elif model == 'TicketType':
            instance = TicketType()
            form = TicketTypeForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Events/TicketType-list/'
        elif model == 'Nomination':
            instance = Nomination()
            prev_counselor = instance.counselor
            form = VenBusinessForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Village%sEmpowerment%sNetwork/Nomination-list/' %('%20','%20')
        elif model == 'FamilyNomination':
            instance = FamilyNomination()
            form = VenFamilyForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Village%sEmpowerment%sNetwork/FamilyNomination-list/' %('%20','%20')
        elif model == 'vbp_book':
            instance = vbp_book()
            form = VBPBookForm(request.POST, instance=instance)
            redirect_url = '/dashboard/Village%sBlack%sPages/vbp_book-list/' %('%20','%20')
        form.save()
        if model == 'Nomination':
            if prev_counselor != instance.counselor:
                subject = "Congratulations! You've Matched With A Village Empowerment Network Counselor!"
                from_email = 'etvnotifications@gmail.com'
                content = render_to_string('counselor-assignment.html',
                {
                    'counselor':instance.counselor,
                    'counsel_link':'https://empowerthevillage.org/village-empowerment-network/schedule/%s' %(instance.ven_id)
                })
                plain_text = 'View email in browser'
                send_mail(subject, plain_text, from_email, [str(instance.nominator_email)], html_message=content)
            else:
                pass
        sweetify.success(request, 'Item Created Successfully!')
        return redirect(redirect_url)

def braintree_disbursements(request):
    disbursements = []
    for x in Disbursement.objects.all():
        disbursements.append(x.get_data)
    p = Paginator(disbursements, 10)
    context = {
        "disbursements": disbursements,
        "p": p
    }
    return render(request, "braintree-dash.html", context)