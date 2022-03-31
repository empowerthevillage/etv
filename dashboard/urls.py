from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', DashboardHome, name="home"),
    path('donor-update', updateDonors)
]
