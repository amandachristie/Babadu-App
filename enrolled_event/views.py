from django.shortcuts import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from datetime import datetime


# Create your views here.
#def show_enrolled_event(request):
cursor.execute(f""" 
    SELECT * from peserta_mendaftar_event;
""")

data_event_didaftar = cursor.fetchall()
    #final_data_kategori_resto = []
'''
for cat in data_kategori_resto:
    cursor.execute(
        f'SELECT * from RESTAURANT_CATEGORY, RESTAURANT R where Rcategory = \'{cat[0]}\''
    )
    canDelete = (len(cursor.fetchall()) == 0)
    tuple_new = cat + (canDelete, )
    final_data_kategori_resto.append(tuple_new)
'''

print(data_event_didaftar)

'''
context = {
    'list_kategori_resto': final_data_kategori_resto,
    'role':request.COOKIES.get('role'),
}
return render(request, "enrolled_event.html", context)
'''

