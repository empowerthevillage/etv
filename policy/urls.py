from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', policy_home, name='policy-home'),
    path('voting/', voting, name='voting'),
]