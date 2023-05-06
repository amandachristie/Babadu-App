from django.urls import path
from daftar_atlet.views import show_daftar_atlet

app_name = 'daftar_atlet'

urlpatterns = [
    path('', show_daftar_atlet, name='show_daftar_atlet'),
]