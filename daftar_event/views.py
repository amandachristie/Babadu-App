from django.shortcuts import render

# Create your views here.
def show_daftar_event(request):
    return render(request, "daftar_event.html")