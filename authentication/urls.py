from django.urls import path
from authentication.views import show_login, show_welcome, show_register, show_register_atlet, show_register_pelatih, show_register_umpire

app_name = 'daftar_sponsor'

urlpatterns = [
    path('login/', show_login, name='show_login'),
    path('', show_welcome, name='show_welcome'),
    path('register/', show_register, name='show_register'),
    path('register-atlet/', show_register_atlet, name='show_register_atlet'),
    path('register-pelatih/', show_register_pelatih, name='show_register_pelatih'),
    path('register-umpire/', show_register_umpire, name='show_register_umpire'),
]