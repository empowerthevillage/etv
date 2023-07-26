from django.urls import path
from .views import *

urlpatterns = [
    path('', health_home, name='health-home'),
    path('phase-one/', health_initiatives, name='health-initiatives'),
    path('village-assist-program/', village_assist, name='village-assist')
]