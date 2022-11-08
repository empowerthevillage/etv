from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('assign-groups', assign_groups),
    path('get-subcategories', get_subcategories, name='get-subcategories'),
    path('get-state/', getStateListings, name='get-state'),
    path('get-filters/', bookFilters, name='get-filters'),
    path('ajax/filter/', filterList, name='filter_list'),
    path('marthas-vineyard/', mv_view),
    path('new-jersey/', nj_view),
    path('new/<state>/filter', listing_filter),
    path('get-counties/<state>', get_counties),
]
