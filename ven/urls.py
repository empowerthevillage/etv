from django.urls import path
from .views import *

urlpatterns = [
    path('', ven_home, name='home'),
    path('notification-email/', ven_email),
    path('welcome-email/', ven_welcome_email),
    path('schedule/<venID>/', ven_schedule),
]
