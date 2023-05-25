from sqlite3 import InternalError
from django.shortcuts import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from enrolled_event.query import *
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.            
def show_enrolled_event(request):
    data_enrolled_event = sql_enrolled_event(request.session['user']['nama'])
    print(data_enrolled_event)

    error_message = messages.get_messages(request)

    if data_enrolled_event is None:
        list_enrolled_event = "Anda tidak memiliki event yang diikuti. Silakan daftar event untuk bertanding."
        context = {
            'list_enrolled_event' : list_enrolled_event,
        }
    else:
        context = {
            'data_enrolled_event' : data_enrolled_event,
        }

    return render(request, "enrolled_event.html", context)

def delete_event(request, nama_event, tahun_event):
    print(nama_event)
    print(tahun_event)

    result = delete((request.session['user']['nama']), nama_event, tahun_event)
    print(result)
    if result != None:
        messages.error(request, result)
        return redirect('/enrolled_event')
    
    return redirect('/enrolled_event')
    
