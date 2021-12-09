from typing import Text
from django.contrib import messages
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from accounts.models import Participant
from .models import *
from vbp.models import *
from vbp.forms import NominationForm
from .forms import RSSForm, STLForm, EFForm
from content.forms import ContactForm
from content.models import contact_submission
from django.core.mail import send_mail

import sweetify

def bingo(request):
    bingo = bingo_card.objects.all()
    contact_form = ContactForm()
    user = request.user
    user_bingo = None
    if user.is_authenticated:
        if user.is_bingo_sponsor or user.is_donor:
            user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    context = {
        'bingo_card': bingo,
        'user_bingo': user_bingo,
        'title': 'Power Bingo | ETV',
        'contact_form': contact_form
    }
    return render(request, "bingo.html", context)

def getTile1(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.field3 = request.POST['field3']
    formobj.field4 = request.POST['field4']
    formobj.save()
    user_bingo.spot1 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile3(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.save()
    user_bingo.spot3 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile4(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.save()
    user_bingo.spot4 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile5(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.save()
    user_bingo.spot5 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile6(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.save()
    user_bingo.spot6 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile7(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.field3 = request.POST['field3']
    formobj.field4 = request.POST['field4']
    formobj.field5 = request.POST['field5']
    formobj.field6 = request.POST['field6']
    formobj.save()
    user_bingo.spot7 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile8(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field1 = request.POST['field2']
    formobj.save()
    user_bingo.spot8 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile9(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.save()
    user_bingo.spot9 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile11(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.save()
    user_bingo.spot11 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile12(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.field3 = request.POST['field3']
    formobj.field4 = request.POST['field4']
    formobj.field5 = request.POST['field5']
    formobj.field6 = request.POST['field6']
    formobj.save()
    user_bingo.spot12 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile14(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field1 = request.POST['field2']
    formobj.save()
    user_bingo.spot14 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile15(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.field3 = request.POST['field3']
    formobj.field4 = request.POST['field4']
    formobj.field5 = request.POST['field5']
    formobj.field6 = request.POST['field6']
    formobj.field7 = request.POST['field7']
    formobj.field8 = request.POST['field8']
    formobj.field9 = request.POST['field9']
    formobj.field10 = request.POST['field10']
    formobj.field11 = request.POST['field11']
    formobj.field12 = request.POST['field12']
    formobj.save()
    user_bingo.spot15 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile17(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.save()
    user_bingo.spot17 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile18(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.field3 = request.POST['field3']
    formobj.field4 = request.POST['field4']
    formobj.field5 = request.POST['field5']
    formobj.save()
    user_bingo.spot18 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile19(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.save()
    user_bingo.spot19 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile20(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.save()
    user_bingo.spot20 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile21(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.save()
    user_bingo.spot21 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile22(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.field3 = request.POST['field3']
    formobj.field4 = request.POST['field4']
    formobj.save()
    user_bingo.spot22 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile23(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.field3 = request.POST['field3']
    formobj.field4 = request.POST['field4']
    formobj.field5 = request.POST['field5']
    formobj.field6 = request.POST['field6']
    formobj.save()
    user_bingo.spot23 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def getTile25(request):
  if request.method == 'POST':
    user = request.user
    user_bingo, created = user_bingo_card.objects.get_or_create(user=user)
    formobj = user_bingo_form()
    formobj.card = user_bingo
    formobj.spot = request.POST['spot']
    formobj.field1 = request.POST['field1']
    formobj.field2 = request.POST['field2']
    formobj.field3 = request.POST['field3']
    formobj.save()
    user_bingo.spot25 = True
    user_bingo.save()
    return HttpResponse('Thank you!')

def nomination_challenge(request):
    if request.method == 'POST':
        nomination_form = NominationForm(request.POST)
        nom_obj = nomination()
        if nomination_form.data['state'] == 'AL':
            obj = vbp_al()
            nom_obj.state = 'AL'
        elif nomination_form.data['state'] == 'AZ':
            obj = vbp_az()
            nom_obj.state = 'AZ'
        elif nomination_form.data['state'] == 'AR':
            obj = vbp_ar()
            nom_obj.state = 'AR'
        elif nomination_form.data['state'] == 'CA':
            obj = vbp_ca()
            nom_obj.state = 'CA'
        elif nomination_form.data['state'] == 'CO':
            obj = vbp_co()
            nom_obj.state = 'CO'
        elif nomination_form.data['state'] == 'CT':
            obj = vbp_ct()
            nom_obj.state = 'CT'
        elif nomination_form.data['state'] == 'DE':
            obj = vbp_de()
            nom_obj.state = 'DE'
        elif nomination_form.data['state'] == 'DC':
            obj = vbp_dc()
            nom_obj.state = 'DC'
        elif nomination_form.data['state'] == 'FL':
            obj = vbp_fl()
            nom_obj.state = 'FL'
        elif nomination_form.data['state'] == 'GA':
            obj = vbp_ga()
            nom_obj.state = 'GA'
        elif nomination_form.data['state'] == 'HI':
            obj = vbp_hi()
            nom_obj.state = 'HI'
        elif nomination_form.data['state'] == 'ID':
            obj = vbp_id()
            nom_obj.state = 'ID'
        elif nomination_form.data['state'] == 'IL':
            obj = vbp_il()
            nom_obj.state = 'IL'
        elif nomination_form.data['state'] == 'IN':
            obj = vbp_in()
            nom_obj.state = 'IN'
        elif nomination_form.data['state'] == 'IA':
            obj = vbp_ia()
            nom_obj.state = 'IA'
        elif nomination_form.data['state'] == 'KS':
            obj = vbp_ks()
            nom_obj.state = 'KS'
        elif nomination_form.data['state'] == 'KY':
            obj = vbp_ky()
            nom_obj.state = 'KY'
        elif nomination_form.data['state'] == 'LA':
            obj = vbp_la()
            nom_obj.state = 'LA'
        elif nomination_form.data['state'] == 'ME':
            obj = vbp_me()
            nom_obj.state = 'ME'
        elif nomination_form.data['state'] == 'MD':
            obj = vbp_md()
            nom_obj.state = 'MD'
        elif nomination_form.data['state'] == 'MA':
            obj = vbp_ma()
            nom_obj.state = 'MA'
        elif nomination_form.data['state'] == 'MI':
            obj = vbp_mi()
            nom_obj.state = 'MI'
        elif nomination_form.data['state'] == 'MN':
            obj = vbp_mn()
            nom_obj.state = 'MN'
        elif nomination_form.data['state'] == 'MS':
            obj = vbp_ms()
            nom_obj.state = 'MS'
        elif nomination_form.data['state'] == 'MO':
            obj = vbp_mo()
            nom_obj.state = 'MO'
        elif nomination_form.data['state'] == 'MT':
            obj = vbp_mt()
            nom_obj.state = 'MT'
        elif nomination_form.data['state'] == 'NE':
            obj = vbp_ne()
            nom_obj.state = 'NE'
        elif nomination_form.data['state'] == 'NV':
            obj = vbp_nv()
            nom_obj.state = 'NV'
        elif nomination_form.data['state'] == 'NH':
            obj = vbp_nh()
            nom_obj.state = 'NH'
        elif nomination_form.data['state'] == 'NJ':
            obj = vbp_nj()
            nom_obj.state = 'NJ'
        elif nomination_form.data['state'] == 'NM':
            obj = vbp_nm()
            nom_obj.state = 'NM'
        elif nomination_form.data['state'] == 'NY':
            obj = vbp_ny()
            nom_obj.state = 'NY'
        elif nomination_form.data['state'] == 'NC':
            obj = vbp_nc()
            nom_obj.state = 'NC'
        elif nomination_form.data['state'] == 'ND':
            obj = vbp_nd()
            nom_obj.state = 'ND'
        elif nomination_form.data['state'] == 'OH':
            obj = vbp_oh()
            nom_obj.state = 'OH'
        elif nomination_form.data['state'] == 'OK':
            obj = vbp_ok()
            nom_obj.state = 'OK'
        elif nomination_form.data['state'] == 'OR':
            obj = vbp_or()
            nom_obj.state = 'OR'
        elif nomination_form.data['state'] == 'PA':
            obj = vbp_pa()
            nom_obj.state = 'PA'
        elif nomination_form.data['state'] == 'RI':
            obj = vbp_ri()
            nom_obj.state = 'RI'
        elif nomination_form.data['state'] == 'SC':
            obj = vbp_sc()
            nom_obj.state = 'SC'
        elif nomination_form.data['state'] == 'SD':
            obj = vbp_sd()
            nom_obj.state = 'SD'
        elif nomination_form.data['state'] == 'TN':
            obj = vbp_tn()
            nom_obj.state = 'TN'
        elif nomination_form.data['state'] == 'TX':
            obj = vbp_tx()
            nom_obj.state = 'TX'
        elif nomination_form.data['state'] == 'UT':
            obj = vbp_ut()
            nom_obj.state = 'UT'
        elif nomination_form.data['state'] == 'VT':
            obj = vbp_vt()
            nom_obj.state = 'VT'
        elif nomination_form.data['state'] == 'VA':
            obj = vbp_va()
            nom_obj.state = 'VA'
        elif nomination_form.data['state'] == 'WA':
            obj = vbp_wa()
            nom_obj.state = 'WA'
        elif nomination_form.data['state'] == 'WV':
            obj = vbp_wv()
            nom_obj.state = 'WV'
        elif nomination_form.data['state'] == 'WI':
            obj = vbp_wi()
            nom_obj.state = 'WI'
        elif nomination_form.data['state'] == 'WY':
            obj = vbp_wy()
            nom_obj.state = 'WY'
        obj.business_name = nomination_form.data['business_name']
        nom_obj.business_name = nomination_form.data['business_name']
        obj.website = nomination_form.data['website']
        obj.city = nomination_form.data['city']
        obj.county = nomination_form.data['county']
        obj.phone = nomination_form.data['phone']
        obj.category = nomination_form.data['category']
        obj.subcategory = nomination_form.data['subcategory']
        obj.approved = 'False'
        if request.user.is_authenticated:
            obj.user = request.user
            obj.team = request.user.team
            obj.nominator_email = request.user.email
            obj.nominator_name = request.user.full_name
            nom_obj.user = request.user
            nom_obj.team = request.user.team
            nom_obj.email = request.user.email
            nom_obj.name = request.user.full_name
        else:
            obj.nominator_email = nomination_form.data['nominator_email']
            obj.nominator_name = nomination_form.data['nominator_name']
            nom_obj.email = nomination_form.data['nominator_email']
            nom_obj.name = nomination_form.data['nominator_name']

        sweetify.success(request, title='Thank you!', icon='success', text='Thank you for nominating a Black-owned business!', button='Nominate Another Business', timer=4000)
        obj.save()
        nom_obj.save()
        return redirect('/black-friday-challenge/nomination-challenge')
    else:
        nomination_form = NominationForm()
    context = {
        'title': 'VBP Nomination Challenge | ETV',
        'nomination_form': nomination_form
    }
    return render(request, 'nomination-challenge.html', context)

def ready_set_shop(request):
    teams = Team.objects.all()
    if request.method == 'POST' and request.user.is_authenticated:
        sweetify.success(request, title='Thank you!', icon='success', text='Thank you for supporting a Black-owned business!', button='Add Another Transaction', timer=7000)
        rss_form = RSSForm(request.POST)
        obj = readysetshop_transaction()
        obj.user = request.user
        obj.first_name = rss_form.data['first_name']
        obj.last_name = rss_form.data['first_name']
        obj.email = request.user.email
        obj.team = request.user.team
        obj.business_name = rss_form.data['business_name']
        obj.amount = rss_form.data['amount']
        obj.date = rss_form.data['date']
        obj.industry = rss_form.data['category']
        if rss_form.data['receipt'] != '':
            obj.receipt_aws = request.FILES['receipt']
        else:
            obj.receipt_aws = None
        obj.save()
        
        send_mail(
            'New Ready, Set, Shop Submission',
            'A new submission has been made for the Ready, Set, Shop Challenge!',
            'admin@empowerthevillage.org',
            ['admin@empowerthevillage.org'],
            fail_silently=True
        )
        return redirect('/black-friday-challenge/ready-set-shop')
    elif request.method == 'POST':
        sweetify.success(request, title='Thank you!', icon='success', text='Thank you for supporting a Black-owned business!', button='Add Another Transaction', timer=7000)
        rss_form = RSSForm(request.POST)
        obj = readysetshop_transaction()
        obj.first_name = rss_form.data['first_name']
        obj.last_name = rss_form.data['first_name']
        obj.email = rss_form.data['email']
        participant = Participant.objects.filter(email=obj.email).first()
        if participant is not None:
            obj.team = participant.team
        else:
            obj.team = None
        obj.business_name = rss_form.data['business_name']
        obj.amount = rss_form.data['amount']
        obj.date = rss_form.data['date']
        obj.industry = rss_form.data['category']
        if rss_form.data['receipt'] != '':
            obj.receipt_aws = request.FILES['receipt']
        else:
            obj.receipt_aws = None
        obj.save()
        send_mail(
            'New Ready, Set, Shop Submission',
            'A new submission has been made for the Ready, Set, Shop Challenge!',
            'admin@empowerthevillage.org',
            ['admin@empowerthevillage.org'],
            fail_silently=True
        )
        return redirect('/black-friday-challenge/ready-set-shop')
    else:
        rss_form = RSSForm()
        contact_form = ContactForm()
    context = {
        'title': 'Ready, Set, Shop | ETV',
        'rss_form': rss_form,
        'contact_form': contact_form,
        'teams': teams
    }
    return render(request, 'ready-set-shop.html', context)

def everyfriday(request):
    if request.method == 'POST':
        rss_form = EFForm(request.POST)
        obj = everyfriday_transaction()
        obj.user = request.user
        obj.business_name = rss_form.data['business_name']
        obj.amount = rss_form.data['amount']
        obj.date = rss_form.data['date']
        obj.industry = rss_form.data['industry']
        obj.receipt_aws = rss_form.data['receipt']
        sweetify.success(request, title='Thank you!', icon='success', text='Thank you for supporting a Black-owned business!', button='Add Another Transaction', timer=4000)
        obj.save()
        return redirect('/black-friday-challenge/ready-set-shop')
    else:
        rss_form = RSSForm()
        contact_form = ContactForm()
    context = {
        'title': 'Ready, Set, Shop | ETV',
        'rss_form': rss_form,
        'contact_form': contact_form,
    }
    return render(request, 'every-friday.html', context)

def spread_the_love(request):
    if request.method == 'POST':
        stl_form = STLForm(request.POST)
        obj = spread_the_love_submission()
        obj.user = request.user
        obj.link = stl_form.data['link']
        
        sweetify.success(request, title='Thank you!', icon='success', text='Thank you for spreading the word!', timer=4000)
        obj.save()
        return redirect('/black-friday-challenge/spread-the-love')
    else:
        stl_form = STLForm()
    context = {
        'title': 'Spread The Love | ETV',
        'stl_form': stl_form,
    }
    return render(request, 'spread_the_love.html', context)

def bf_home(request):
    context = {
        'title': 'ETV | Black Friday Challenge'
    }
    return render(request, 'bf_home.html', context)