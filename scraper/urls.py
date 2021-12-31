from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', scraper, name='home'),
    path('get-sbo', create_sbo_objects, name='sbo'),
]
