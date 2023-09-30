from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Flyer


def policy_home(request):
    context = {
        'title': 'ETV | Policy & Power',
    }
    return render(request, "policy_home.html", context)

def voting(request):
    context = {
        'title': 'ETV | Operation Ballot Box',
        'flyers': Flyer.objects.filter(active=True)
    }
    return render(request, "voting.html", context)

def voting_print(request):
    context = {
        'title': 'ETV | Operation Ballot Box',
    }
    return render(request, "voting_print.html", context)

def obb_flyer(request, state):
    published_states = ['az', 'tx', 'ar', 'la', 'ga', 'fl', 'nc', 'ky', 'oh', 'mi', 'wi', 'pa', 'md', 'nj']
    state_formatted = str(state).lower()
    if state_formatted in published_states:
        url = 'https://empowerthevillage.s3.amazonaws.com/static/img/operation-ballot-box/%s-web.pdf' %(state_formatted)
        return redirect(url)
    else:
        return redirect('/policy-and-power/voting/')
    