from django.shortcuts import render
from django.db import connection

# Create your views here.
def show_list_event(request):
    cursor4 = connection.cursor()
    cursor4.execute("SET SEARCH_PATH TO babadu")
    cursor4.execute("SELECT e.nama_event, e.tahun, e.nama_stadium, STRING_AGG(pk.jenis_partai, ', ') AS jenis_partai, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, s.kapasitas FROM event e JOIN stadium s ON e.nama_stadium = s.nama JOIN (SELECT DISTINCT nama_event, jenis_partai FROM partai_kompetisi) pk ON e.nama_event = pk.nama_event GROUP BY e.nama_event, e.tahun, e.nama_stadium, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, s.kapasitas;") 
    result = cursor4.fetchall()
    list_event = []
    for event in result:
        list_event.append({
            "nama_event" : event[0],
            "tahun" : event[1],
            "nama_stadium" : event[2],
            "jenis_partai" : event[3],
            "kategori_superseries": event[4],
            "tgl_mulai" : event[5],
            "tgl_selesai": event[6],
            "kapasitas" : event[7],
        })
    context = {'data': list_event
    }
                
    # context2 = {'data2': list_atlet2}
    return render(request, "list_event.html",context)