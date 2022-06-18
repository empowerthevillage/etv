from django.urls import path
from .views import *

urlpatterns = [
    path('', policy_home, name='policy-home'),
    path('voting/', voting, name='voting'),
]