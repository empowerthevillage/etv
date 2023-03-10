from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('run-analytics/', analytics),
    path('get-subcategories', get_subcategories, name='get-subcategories'),
    path('get-state/', getStateListings, name='get-state'),
    path('get-filters/', bookFilters, name='get-filters'),
    path('get-subcats/', get_subcats),
    path('ajax/filter/', filterList, name='filter_list'),
    path('marthas-vineyard/', mv_view),
    path('holiday-gift-guide/', gift_guide_view),
    path('holiday-gift-guide-2/', gift_guide_2_view),
    path('new-jersey/', nj_view),
    path('essex-county/', essex_view),
    path('morris-county/', morris_view),
    path('nj-filter-new/', nj_filter_new),
    path('new/<state>/filter', listing_filter),
    path('get-counties/<state>', get_counties),
]
