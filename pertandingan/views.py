from django.shortcuts import render

# Create your views here.
def show_pertandingan(request):
    return render(request, "pertandingan.html")