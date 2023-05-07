from django.urls import path
from daftar_event.views import show_daftar_event

app_name = 'dashboard'

urlpatterns = [
    path('', show_daftar_event, name='show_daftar_event'),
]