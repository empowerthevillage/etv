from django.urls import path
from .views import *

urlpatterns = [
    path('', scraper, name='home'),
    path('get-sbo', create_sbo_objects, name='sbo'),
]
