from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('get-subcategories', get_subcategories, name='get-subcategories'),
    path('get-state/', getStateListings, name='get-state'),
    path('get-filters/', bookFilters, name='get-filters'),
    path('ajax/filter/', filterList, name='filter_list'),
    path('new/<state>/filter', listing_filter),
    path('get-counties/<state>', get_counties),
]
