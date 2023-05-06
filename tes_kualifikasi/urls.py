from django.urls import path
from tes_kualifikasi.views import show_tes_kualifikasi

app_name = 'tes_kualifikasi'

urlpatterns = [
    path('', show_tes_kualifikasi, name='show_tes_kualifikasi'),
]