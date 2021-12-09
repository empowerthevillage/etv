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

def education_phase_one(request):
    context = {
        'title': 'ETV | Education & Employment Phase One',
    }
    return render(request, "education_phase_one.html", context)
