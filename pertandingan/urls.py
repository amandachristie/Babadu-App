from django.urls import path
from pertandingan.views import show_pertandingan
app_name = 'pertandingan'

urlpatterns = [
    path('', show_pertandingan, name='show_pertandingan'),
]