from django.urls import path
from daftar_atlet.views import *

app_name = 'daftar_atlet'

urlpatterns = [
    path('', show_daftar_atlet, name='show_daftar_atlet'),
    path('list_atlet/', show_list_atlet, name='show_list_atlet'),
]