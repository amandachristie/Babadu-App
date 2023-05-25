from sqlite3 import InternalError
from django.shortcuts import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from enrolled_event.query import *
from datetime import datetime


# Create your views here.            
def show_enrolled_event(request):
    data_enrolled_event = SQLenrolledEvent(request.session['user']['nama'])
    print(data_enrolled_event)

    context = {
        'data_enrolled_event' : data_enrolled_event
    }
    return render(request, "enrolled_event.html", context)

def delete_event(request, nama_event, tahun_event):
    print(nama_event)
    print(tahun_event)

    result = delete((request.session['user']['nama']), nama_event, tahun_event)
    if result != None:
        data_enrolled_event = SQLenrolledEvent(request.session['user']['nama'])
        context = {
            'data_enrolled_event' : data_enrolled_event,
            'error_message': result
        }
        return render(request, 'enrolled_event.html', context)
    
    show_enrolled_event()
    
