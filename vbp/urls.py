from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('get-subcategories', get_subcategories, name='get-subcategories'),
    path('get-state/', getStateListings, name='get-state'),
    path('get-filters/', bookFilters, name='get-filters'),
    path('ajax/filter/', filterList, name='filter_list'),
    path('ct/filter/', ct_list, name='ct_list'),
    path('ny/filter/', ny_list, name='ny_list'),
    path('nj/filter/', nj_list, name='nj_list'),
    path('ma/filter/', ma_list, name='ma_list'),
    path('va/filter/', va_list, name='va_list'),
    path('pa/filter/', pa_list, name='pa_list'),
    path('oh/filter/', oh_list, name='oh_list'),
    path('md/filter/', md_list, name='md_list'),
    path('dc/filter/', dc_list, name='dc_list'),
    path('de/filter/', de_list, name='de_list'),
    path('decounties/', get_counties_de, name='decounties'),
    path('ctcounties/', get_counties_ct, name='ctcounties'),
    path('nycounties/', get_counties_ny, name='nycounties'),
    path('njcounties/', get_counties_nj, name='njcounties'),
    path('macounties/', get_counties_ma, name='macounties'),
    path('vacounties/', get_counties_va, name='vacounties'),
    path('pacounties/', get_counties_pa, name='pacounties'),
    path('ohcounties/', get_counties_oh, name='ohcounties'),
    path('mdcounties/', get_counties_md, name='mdcounties'),
]
