from django.urls import path
from .views import *

urlpatterns = [
    path('', walker_home, name='home'),
    path('register/', walker_registration, name='registration'),
    path('organization-registration/', org_registration, name='org-registration'),
    path('process-walker-donation/', process_walker_donation, name='process-walker-donation'),
    path('sponsor/', sponsor, name='sponsor'),
    path('support-a-walker/', sponsor_walker, name="support-walker"),
    path('walker-donation/', walker_donation_form, name="walker-donation-form"),
    path('<org>/<walker>/', org_walker_detail, name='group-walker-detail'),
    path('<walker>/', walker_detail, name='walker-detail'),
]
