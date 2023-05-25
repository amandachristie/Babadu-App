from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', welcome, name='welcome'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout')
]