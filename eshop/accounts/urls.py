from django.urls import path
from .views import *

urlpatterns = [
    path('send/register/vercode', send_code),
    path('send/changepasswordorphone/vercode', send_code_change_password_or_phone),
    path('customer/register', register_customer),
    path('customer/login', customer_login_view),
    path('customer/changepassword', change_password),
    path('customer/changephone', change_phone),
    path('customer/editinfo', CustomerProfileUpdateView.as_view())
]