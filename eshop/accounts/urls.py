from django.urls import path
from .views import *

urlpatterns = [
    path('send/vercode', send_code),
    path('customer/register', register_customer),
    path('customer/login', customer_login_view)
]