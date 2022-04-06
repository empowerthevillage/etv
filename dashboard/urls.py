from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', DashboardHome, name="home"),
    path('donor-update/', updateDonors),
    path('<appname>/', appHome, name="app"),
    path('<appname>/<model>-list/', modelHome, name="model"),
    path('<appname>/<model>-list/edit/<pk>', objectChange, name="change"),
]
