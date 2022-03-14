from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings

import sweetify

def education_home(request):
    context = {
        'title': 'ETV | Education & Employment',
    }
    return render(request, "education_home.html", context)

def village_at_work(request):
    context = {
        'title': 'ETV | Village@Work',
    }
    return render(request, "village_at_work.html", context)

def village_strivers(request):
    context = {
        'title': 'ETV | Village Strivers',
    }
    return render(request, "village_strivers.html", context)
