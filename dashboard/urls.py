from django.urls import path
from dashboard.views import show_dashboard

app_name = 'dashboard'

urlpatterns = [
    path('', show_dashboard, name='show_dashboard'),
]