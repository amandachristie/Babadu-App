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

def delete_event(request):
    print('delete')
    return 1
