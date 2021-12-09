"""etv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from accounts.admin import admin_site

from .views import *
from accounts.views import LoginView, RegisterView, GuestRegisterView
from vbp.views import home
from content.views import efbf, efbf_subscribed, contact, mailchimp_signup

from vbp.models import *
from ven.views import *

Alabama = vbp_al.objects.filter(approved=False).count()
Alaska = vbp_ak.objects.filter(approved=False).count()
Arizona = vbp_az.objects.filter(approved=False).count()
Arkansas = vbp_ar.objects.filter(approved=False).count()
California = vbp_ca.objects.filter(approved=False).count()
Colorado = vbp_co.objects.filter(approved=False).count()
Connecticut = vbp_ct.objects.filter(approved=False).count()
Delaware = vbp_de.objects.filter(approved=False).count()
DistrictofColumbia = vbp_dc.objects.filter(approved=False).count()
Florida = vbp_fl.objects.filter(approved=False).count()
Georgia = vbp_ga.objects.filter(approved=False).count()
Hawaii = vbp_hi.objects.filter(approved=False).count()
Idaho = vbp_id.objects.filter(approved=False).count()
Illinois = vbp_il.objects.filter(approved=False).count()
Indiana = vbp_in.objects.filter(approved=False).count()
Iowa = vbp_ia.objects.filter(approved=False).count()
Kansas = vbp_ks.objects.filter(approved=False).count()
Kentucky = vbp_ky.objects.filter(approved=False).count()
Louisiana = vbp_la.objects.filter(approved=False).count()
Maine = vbp_me.objects.filter(approved=False).count()
Maryland = vbp_md.objects.filter(approved=False).count()
Massachusetts = vbp_ma.objects.filter(approved=False).count()
Michigan = vbp_mi.objects.filter(approved=False).count()
Minnesota = vbp_mn.objects.filter(approved=False).count()
Mississippi = vbp_ms.objects.filter(approved=False).count()
Missouri = vbp_mo.objects.filter(approved=False).count()
Montana = vbp_mt.objects.filter(approved=False).count()
Nebraska = vbp_ne.objects.filter(approved=False).count()
Nevada = vbp_nv.objects.filter(approved=False).count()
NewHampshire = vbp_nh.objects.filter(approved=False).count()
NewJersey = vbp_nj.objects.filter(approved=False).count()
NewMexico = vbp_nm.objects.filter(approved=False).count()
NewYork = vbp_ny.objects.filter(approved=False).count()
NorthCarolina = vbp_nc.objects.filter(approved=False).count()
NorthDakota = vbp_nd.objects.filter(approved=False).count()
Ohio = vbp_oh.objects.filter(approved=False).count()
Oklahoma = vbp_ok.objects.filter(approved=False).count()
Oregon = vbp_or.objects.filter(approved=False).count()
Pennsylvania = vbp_pa.objects.filter(approved=False).count()
RhodeIsland = vbp_ri.objects.filter(approved=False).count()
SouthCarolina = vbp_sc.objects.filter(approved=False).count()
SouthDakota = vbp_sd.objects.filter(approved=False).count()
Tennessee = vbp_tn.objects.filter(approved=False).count()
Texas = vbp_tx.objects.filter(approved=False).count()
Utah = vbp_ut.objects.filter(approved=False).count()
Vermont = vbp_vt.objects.filter(approved=False).count()
Virginia = vbp_va.objects.filter(approved=False).count()
Washington = vbp_wa.objects.filter(approved=False).count()
WestVirginia = vbp_wv.objects.filter(approved=False).count()
Wisconsin = vbp_wi.objects.filter(approved=False).count()
Wyoming = vbp_wy.objects.filter(approved=False).count()

urlpatterns = [
    path('contact/', contact, name='contact' ),
    path('myadmin/etvadmin209423/', admin_site.urls, {'extra_context': {
        'AL': Alabama,
        'AK': Alaska,
        'AZ': Arizona,
        'AR': Arkansas,
        'CA': California,
        'CO': Colorado,
        'CT': Connecticut,
        'DE': Delaware,
        'DC': DistrictofColumbia,
        'FL': Florida,
        'GA': Georgia,
        'HI': Hawaii,
        'ID': Idaho,
        'IL': Illinois,
        'IN': Indiana,
        'IA': Iowa,
        'KS': Kansas,
        'KY': Kentucky,
        'LA': Louisiana,
        'ME': Maine,
        'MD': Maryland,
        'MA': Massachusetts,
        'MI': Michigan,
        'MN': Minnesota,
        'MS': Mississippi,
        'MO': Missouri,
        'MT': Montana,
        'NE': Nebraska,
        'NV': Nevada,
        'NH': NewHampshire,
        'NJ': NewJersey,
        'NM': NewMexico,
        'NY': NewYork,
        'NC': NorthCarolina,
        'ND': NorthDakota,
        'OH': Ohio,
        'OK': Oklahoma,
        'OR': Oregon,
        'PA': Pennsylvania,
        'RI': RhodeIsland,
        'SC': SouthCarolina,
        'SD': SouthDakota,
        'TN': Tennessee,
        'TX': Texas,
        'UT': Utah,
        'VT': Vermont,
        'VA': Virginia,
        'WA': Washington,
        'WV': WestVirginia,
        'WI': Wisconsin,
        'WY': Wyoming,
    }}, name='myadmin', ),
    path('', home_page, name='home'),
    path('privacy-policy', privacy, name="privacy"),
    path('terms-and-conditions', terms, name="terms"),
    path('about/', about_page, name='about'),
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include(("accounts.urls", "accounts"), namespace='account')),
    path('accounts/', include("accounts.passwords.urls")),
    path('black-friday-challenge/', include(("bfchallenge.urls", "bfchallenge"), namespace='bfchallenge')),
    path('billing/', include(("billing.urls", "billing"), namespace='billing')),
    path('cart/', include(("carts.urls", "carts"), namespace='carts')),
    path('donation/', include(("donations.urls", "donations"), namespace='donation')),
    path('economic-prosperity/', economic_prosperity, name='prosperity'),
    path('events/', include(("events.urls", "events"), namespace='events')),
    path('news-and-events/', news, name='news'),
    path('shop/', shop, name='shop'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOUGOUT_REDIRECT_URL), name='logout'),
    path('make-every-friday-black-friday/', efbf, name='efbf'),
    path('mailchimp-signup/', mailchimp_signup, name='mailchimp-signup'),
    path('merchandise/', include(("merchandise.urls", "merchandise"), namespace='merchandise')),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/guest', GuestRegisterView.as_view(), name='guest_register'),
    path('settings/', RedirectView.as_view(url='/account')),
    path('strategic-pillars/', strategic_pillars, name='pillars'),
    path('village-black-pages/', include(("vbp.urls", "vbp"), namespace='vbp')),
    path('', include('social_django.urls', namespace='social')),
    path('health-and-wellness/', include(("health.urls", "health"), namespace='health')),
    path('policy-and-power/', include(("policy.urls", "policy"), namespace='policy')),
    path('education-and-employment/', include(("education.urls", "education"), namespace='education')),
    path('village-empowerment-network-nomination', venForm, name='ven-nomination'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
