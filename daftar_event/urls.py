from django.urls import path
from daftar_event.views import *

app_name = 'dashboard'

urlpatterns = [
    path('', show_daftar_stadium, name='show_daftar_stadium'),
    path('event/', show_daftar_event, name='show_daftar_event'),
    path('event/kategori/', show_daftar_kategori, name='show_daftar_kategori'),
]