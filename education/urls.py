from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', education_home, name='education-home'),
    path('phase-one/', education_phase_one, name='education-phase-one'),
]