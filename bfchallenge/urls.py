from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('bingo', bingo, name='bingo'),
    path('nomination-challenge', nomination_challenge, name='nomination'),
    path('ready-set-shop', ready_set_shop, name='readyss'),
    path('spread-the-love', spread_the_love, name='stl'),
    path('everyfriday', everyfriday, name='everyfriday'),
    path('', bf_home, name='home'),
    path('spot-1', getTile1, name='spot-1'),
    path('spot-3', getTile3, name='spot-3'),
    path('spot-4', getTile4, name='spot-4'),
    path('spot-5', getTile5, name='spot-5'),
    path('spot-6', getTile6, name='spot-6'),
    path('spot-7', getTile7, name='spot-7'),
    path('spot-8', getTile8, name='spot-8'),
    path('spot-9', getTile9, name='spot-9'),
    path('spot-11', getTile11, name='spot-11'),
    path('spot-12', getTile12, name='spot-12'),
    path('spot-14', getTile14, name='spot-14'),
    path('spot-15', getTile15, name='spot-15'),
    path('spot-17', getTile17, name='spot-17'),
    path('spot-18', getTile18, name='spot-18'),
    path('spot-19', getTile19, name='spot-19'),
    path('spot-20', getTile20, name='spot-20'),
    path('spot-21', getTile21, name='spot-21'),
    path('spot-22', getTile22, name='spot-22'),
    path('spot-23', getTile23, name='spot-23'),
    path('spot-25', getTile25, name='spot-25'),
]