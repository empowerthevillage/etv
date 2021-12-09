from django.urls import path
from django.conf.urls import url
from .views import RegisterView, AccountHomeView, JoinTeam

urlpatterns = [
    path('my-account/', AccountHomeView, name='home'),
    path('join-team/', JoinTeam, name='jointeam')
]
