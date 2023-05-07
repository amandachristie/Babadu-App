from django.shortcuts import render

# Create your views here.
def show_daftar_atlet(request):
    return render(request, "daftar_atlet.html")

def show_list_atlet(request):
    return render(request, "list_atlet.html")