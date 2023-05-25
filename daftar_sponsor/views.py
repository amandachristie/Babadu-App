from django.shortcuts import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from daftar_sponsor.query import *
from datetime import datetime


# Create your views here.
def show_daftar_sponsor(request):
    data_sponsor_available = sql_daftar_sponsor_available(request.session['user']['nama'])
    print(data_sponsor_available)

    context = {
        'data_sponsor_available' : data_sponsor_available
    }

    if request.method == 'POST':
        nama_sponsor = request.POST['sponsor']
        tgl_mulai = request.POST['tglMulai']
        tgl_selesai = request.POST['tglSelesai']

        if not (nama_sponsor and tgl_mulai and tgl_selesai):
            error_message = "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu"
            context = {
                    'data_sponsor_available' : data_sponsor_available,
                    'error_message': error_message
            }
            return render(request, "daftar_sponsor.html", context)
        
        sql_daftar_sponsor((request.session['user']['nama']), nama_sponsor, tgl_mulai, tgl_selesai)
        return redirect('list/')
    

    return render(request, "daftar_sponsor.html", context)

def show_list_sponsor(request):
    data_list_sponsor = sql_list_sponsor(request.session['user']['nama'])
    print(data_list_sponsor)

    context = {
        'data_list_sponsor' : data_list_sponsor
    }
    return render(request, "list_sponsor.html", context)