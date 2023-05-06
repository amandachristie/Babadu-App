from django.shortcuts import render

# Create your views here.
def show_form_kualifikasi(request):
    return render(request, "form_kualifikasi.html")

def show_pertanyaan_kualifikasi(request):
    return render(request, "pertanyaan_kualifikasi.html")