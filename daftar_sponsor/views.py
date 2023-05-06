from django.shortcuts import render

# Create your views here.
def show_daftar_sponsor(request):
    return render(request, "daftar_sponsor.html")