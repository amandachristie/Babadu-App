from django.urls import path
from tes_kualifikasi.views import *

app_name = 'tes_kualifikasi'

urlpatterns = [
    path('', show_form_kualifikasi, name='show_form_kualifikasi'),
    path('pertanyaan_kualifikasi/', show_pertanyaan_kualifikasi, name='show_pertanyaan_kualifikasi'),
]