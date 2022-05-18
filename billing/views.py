from telnetlib import STATUS
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.transaction import atomic, non_atomic_requests
from django.http.response import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Disbursement

import json

gateway = settings.GATEWAY

@csrf_exempt
@require_POST
def braintree_disbursement(request):
    print('no error before gateway')
    print(request)
    return HttpResponse(status=200)