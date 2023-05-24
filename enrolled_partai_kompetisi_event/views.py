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

    context = {
        'data_enrolled_partai_kompetisi_event' : data_enrolled_partai_kompetisi_event
    }
    return render(request, "enrolled_partai_kompetisi_event.html", context)