from django.shortcuts import render

# Create your views here.
def show_tes_kualifikasi(request):
    return render(request, "tes_kualifikasi.html")