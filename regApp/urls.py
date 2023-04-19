

from django.urls import path 
from .views import *
urlpatterns = [
    path('' ,home,name='home'),
    path('nav_to_register_page/',nav_to_register_page,name='nav_to_register_page'),
    path('nav_to_login_page/',nav_to_login_page,name='nav_to_login_page'),
    path('nav_to_otp_page/',nav_to_otp_page,name='nav_to_otp_page'),
    path('signup/',signup_view,name='signup'),
    path('verify_otp/',verify_otp,name='verify_otp'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout')
]
