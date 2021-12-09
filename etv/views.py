from django.shortcuts import render, redirect
from ven.forms import BusinessForm
from accounts.models import Team

def home_page(request):
    form = BusinessForm()
    context = {
        'nomination_form': form,
        'title':'ETV | Home',
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
        'title': 'ETV | Economic Prosperity',
    }
    return render(request, "prosperity.html", context)

def news(request):
    context = {
    'title':'ETV | News & Events'
    }
    return render(request, "news.html", context)

def shop(request):
    context = {
        'title': 'ETV | Shop',
    }
    return render(request, "shop.html", context)
