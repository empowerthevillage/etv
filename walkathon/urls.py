from django.urls import path
from .views import *

urlpatterns = [
    path('', walker_home, name='home'),
    path('<walker>/', walker_detail, name='walker-detail'),
]
