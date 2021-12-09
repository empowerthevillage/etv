from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', donate, name='donate'),
    path('create', donation_create, name='create'),
    path('review', donation_review, name='review'),
    path('complete', donation_complete, name='complete'),
    path('analytics', donation_analytics, name="analytics")
]