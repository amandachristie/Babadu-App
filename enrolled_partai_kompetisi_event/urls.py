from django.urls import path
from enrolled_partai_kompetisi_event.views import *

urlpatterns = [
    path('', show_enrolled_partai_kompetisi_event, name='show_enrolled_partai_kompetisi_event'),
]