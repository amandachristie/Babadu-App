from django.urls import path
from daftar_sponsor.views import *

app_name = 'daftar_sponsor'

urlpatterns = [
    path('', show_daftar_sponsor, name='show_daftar_sponsor'),
    path('list/', show_list_sponsor, name='show_list_sponsor'),
]
