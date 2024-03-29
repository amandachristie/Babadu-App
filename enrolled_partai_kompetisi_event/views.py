from django.shortcuts import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from enrolled_partai_kompetisi_event.query import *
from datetime import datetime


# Create your views here.            
def show_enrolled_partai_kompetisi_event(request):
    cursor = connection.cursor()
    data_enrolled_partai_kompetisi_event = sql_enrolled_partai_kompetisi_event(request.session['user']['nama'])
    print(data_enrolled_partai_kompetisi_event)

    if data_enrolled_partai_kompetisi_event is None:
        list_partai_kompetisi = "Anda tidak memiliki partai kompetisi event yang diikuti. Silakan daftar event untuk bertanding."
        context = {
            'list_partai_kompetisi' : list_partai_kompetisi,
        }
    else:
        context = {
            'data_enrolled_partai_kompetisi_event' : data_enrolled_partai_kompetisi_event
        }

    return render(request, "enrolled_partai_kompetisi_event.html", context)