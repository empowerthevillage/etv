from django.urls import path
from .views import *

urlpatterns = [
    path('', policy_home, name='policy-home'),
    path('voting/', voting, name='voting'),
    path('village-strivers-application/', strivers_application, name='stivers-application')

]