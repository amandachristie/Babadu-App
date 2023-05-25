from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', main_auth, name='main_auth'),
    path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path('logout/', user_logout, name='user_logout')
]