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
