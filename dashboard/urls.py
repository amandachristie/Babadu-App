from django.urls import path
from dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    path('', base, name='base'),
    path('profil/', dashboard, name='dashboard'),
]