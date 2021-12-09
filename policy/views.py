from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings

import sweetify

def policy_home(request):
    context = {
        'title': 'ETV | Policy & Power',
    }
    return render(request, "policy_home.html", context)

def voting(request):
    context = {
        'title': 'ETV | Voting',
    }
    return render(request, "voting.html", context)
