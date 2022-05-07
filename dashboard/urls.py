from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', DashboardHome, name="home"),
    path('create/', new_obj, name="save-new"),
    path('delete/', delete_obj, name="delete"),
    path('save/', save_obj, name="save"),
    path('donor-update/', updateDonors),
    path('<category>/', appHome, name="category"),
    path('<category>/<model>-list/', modelHome, name="model"),
    path('<category>/<model>-list/edit/<pk>', objectChange, name="change"),
    path('<category>/<model>-list/create/', objectNew, name="new"),
    path('<category>/<model>-list/view/<pk>', objectView, name="view"),
]
