from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings

import sweetify

def health_home(request):
    context = {
        'title': 'ETV | Health & Wellness',
    }
    return render(request, "health_home.html", context)

def health_initiatives(request):
    context = {
        'title': 'ETV | Health & Wellness Phase One Initiatives',
    }
    return render(request, "phase_one_initiatives.html", context)
