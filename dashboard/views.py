from django.shortcuts import render

# Create your views here.
def show_dashboard(request):
    return render(request, "dashboard.html")

def show_dashboard_atlet(request):
    return render(request, "dashboard_atlet.html")

def show_dashboard_pelatih(request):
    return render(request, "dashboard_pelatih.html")

def show_dashboard_umpire(request):
    return render(request, "dashboard_umpire.html")