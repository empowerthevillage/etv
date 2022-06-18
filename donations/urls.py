from django.urls import path
from .views import *

urlpatterns = [
    path('', donate, name='donate'),
    path('create/', donation_create, name='create'),
    path('review/', donation_review, name='review'),
    path('complete/', donation_complete, name='complete'),
    path('analytics/', donation_analytics, name="analytics"),
    path('express-review/', express_review, name="express-review"),
    path('email-test/', mail_test, name='test-mail'),
    path('send-mail/', send_test_email, name="send-mail"),
    path('update-donors/', update_donors)
]