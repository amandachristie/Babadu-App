from django.urls import path
from list_event.views import show_list_event

app_name = 'list_event'

urlpatterns = [
    path('', show_list_event, name='show_list_event'),
]