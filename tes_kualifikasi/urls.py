from django.urls import path
from tes_kualifikasi.views import *

app_name = 'kualifikasi'

urlpatterns = [
    path('', show_list_kualifikasi, name='show_list_kualifikasi'),
    path('form/', show_form_kualifikasi, name='show_form_kualifikasi'),
    path('pertanyaan_kualifikasi/<int:tahun>/<int:batch>/<str:tempat>/<str:tanggal>', show_pertanyaan_kualifikasi, name='show_pertanyaan_kualifikasi'),
    path('riwayat_kualifikasi/', show_riwayat_kualifikasi, name='show_riwayat_kualifikasi'),
]