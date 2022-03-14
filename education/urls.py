from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', education_home, name='education-home'),
    path('village-at-work/', village_at_work, name='village-at-work'),
    path('village-strivers/', village_strivers, name='village-strivers'),
]