from django.urls import path
from .views import *

urlpatterns = [
    path('', economic_prosperity, name="home"),
    path('village-at-work/', village_at_work, name='village-at-work'),
    
]