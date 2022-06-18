from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList, name='list'),
    path('add-to-cart', AddToCart, name='add-to-cart'),
    path('remove-from-cart', RemoveFromCart, name='remove-from-cart')
]
