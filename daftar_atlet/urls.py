from django.urls import path
from daftar_atlet.views import *

app_name = 'daftar_atlet'

urlpatterns = [
    path('daftar_atlet/', show_daftar_atlet, name='show_daftar_atlet'),
    path('list_atlet/', show_list_atlet, name='show_list_atlet'),
    path('list_atlet_umpire/', show_list_atlet_umpire, name='show_list_atlet_umpire'),
]