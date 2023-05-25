from django.urls import path
from daftar_event.views import *

app_name = 'daftar_event'

urlpatterns = [
    path('', show_daftar_stadium, name='show_daftar_stadium'),
    path('event/<str:stadium_nama>/', show_daftar_event, name='show_daftar_event'),
    path('event/<str:stadium_nama>/kategori/<str:event_nama>/', show_daftar_kategori, name='show_daftar_kategori'),
]