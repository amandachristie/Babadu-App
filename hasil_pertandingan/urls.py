from django.urls import path
from hasil_pertandingan.views import show_hasil_pertandingan
app_name = 'hasil_pertandingan'

urlpatterns = [
    path('', show_hasil_pertandingan, name='show_hasil_pertandingan'),
]