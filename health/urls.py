from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', health_home, name='health-home'),
    path('phase-one/', health_initiatives, name='health-initiatives'),
]