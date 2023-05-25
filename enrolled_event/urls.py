from django.urls import path
from enrolled_event.views import *
app_name = 'enrolled_event'

urlpatterns = [
    path('', show_enrolled_event, name='show_enrolled_event'),
    path('delete_event/<str:nama_event>/<str:tahun_event>/', delete_event, name='delete_event'),
]