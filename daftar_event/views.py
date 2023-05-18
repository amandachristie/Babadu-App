from django.shortcuts import render

# Create your views here.
def show_daftar_stadium(request):
    return render(request, "daftar_stadium.html")

def show_daftar_event(request):
    return render(request, "daftar_event.html")

def show_daftar_kategori(request):
    return render(request, "daftar_kategori.html")