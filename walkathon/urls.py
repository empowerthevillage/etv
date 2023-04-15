from django.urls import path
from .views import *

urlpatterns = [
    path('', walker_home, name='home'),
    path('register/', walker_registration, name='registration'),
    path('organization-registration/', org_registration, name='org-registration'),
    path('<walker>/', walker_detail, name='walker-detail'),
]
