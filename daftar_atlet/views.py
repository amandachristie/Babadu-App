from django.shortcuts import render

# Create your views here.
def show_daftar_atlet(request):
    return render(request, "daftar_atlet.html")