from django.shortcuts import render
from django.db import connection
# Create your views here.
# def show_hasil_pertandingan(request):
#     return render(request, "hasil_pertandingan.html")

def show_hasil_pertandingan(request):
    cursor5 = connection.cursor()
    cursor5.execute("SET SEARCH_PATH TO babadu")
    cursor5.execute("SELECT m.nama_event, STRING_AGG(CASE WHEN pk.ID_Atlet_Ganda IS NOT NULL THEN CONCAT(m1.nama, ' & ', m2.nama) ELSE m1.nama END, ', ') AS nama_tim, pm.jenis_babak FROM peserta_mengikuti_match pm JOIN match m ON pm.jenis_babak = m.jenis_babak JOIN peserta_kompetisi pk ON pm.nomor_peserta = pk.nomor_peserta LEFT JOIN member m1 ON pk.ID_Atlet_Kualifikasi = m1.id LEFT JOIN member m2 ON pk.ID_Atlet_Ganda = m2.id GROUP BY m.nama_event, pm.jenis_babak ORDER BY m.nama_event, pm.jenis_babak;") 
    result5 = cursor5.fetchall()
    list_babak = []
    for babak in result5:
        list_babak.append({
            "nama_event" : babak[0],
            "nama_tim" : babak[1],
            "jenis_babak" : babak[2],
        })
    for pertandingan in list_babak:
        print(pertandingan["nama_event"])


    cursor4 = connection.cursor()
    cursor4.execute("SET SEARCH_PATH TO babadu")
    cursor4.execute("SELECT e.nama_event, e.tahun, e.nama_stadium, e.total_hadiah,STRING_AGG(pk.jenis_partai, ', ') AS jenis_partai, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, s.kapasitas FROM event e JOIN stadium s ON e.nama_stadium = s.nama JOIN (SELECT DISTINCT nama_event, jenis_partai FROM partai_kompetisi) pk ON e.nama_event = pk.nama_event GROUP BY e.nama_event, e.tahun, e.nama_stadium,e.total_hadiah, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, s.kapasitas;") 
    result = cursor4.fetchall()
    list_event = []
    for event in result:
        list_gabung = []
        for pertandingan in list_babak:
            if event[0] == pertandingan["nama_event"]:
                list_gabung.append(pertandingan)
        list_event.append({
            "nama_event" : event[0],
            "tahun" : event[1],
            "nama_stadium" : event[2],
            "total_hadiah" : event[3],
            "jenis_partai" : event[4],
            "kategori_superseries": event[5],
            "tgl_mulai" : event[6],
            "tgl_selesai": event[7],
            "kapasitas" : event[8],
            "list_gabung" :list_gabung
        })
    
    for event in list_event:
        print(event)

    
    context = {'data': list_event, 'data2' :list_babak}
                
    # context2 = {'data2': list_atlet2}
    return render(request, "hasil_pertandingan.html",context)
