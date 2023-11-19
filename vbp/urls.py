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
    path('montclair/', montclair_view),
    path('montclair-county/',montclair_view),
    path('holiday-gift-guide/', gift_guide_view),
    path('holiday-gift-guide-2/', gift_guide_2_view),
    path('2023-holiday-gift-guide/', gift_guide_2023),
    path('nj-filter-new/', nj_filter_new),
    path('new/<state>/filter', listing_filter),
    path('get-counties/<state>', get_counties),
    path('<slug>/', individual_state_view),
    path('<state_slug>/<slug>/', individual_book_view),
]
