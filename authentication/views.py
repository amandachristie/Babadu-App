from django.shortcuts import render

# Create your views here.
def show_login(request):
    return render(request, "login.html")

def show_welcome(request):
    return render(request, "welcome.html")

def show_register(request):
    return render(request, "register.html")

def show_register_atlet(request):
    return render(request, "register_atlet.html")

def show_register_umpire(request):
    return render(request, "register_umpire.html")

def show_register_pelatih(request):
    return render(request, "register_pelatih.html")