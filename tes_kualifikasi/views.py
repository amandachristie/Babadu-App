from django.shortcuts import render
from utils.query import query
from django.shortcuts import render, redirect
from authentication.views import *

# Create your views here.

#umpire
#Constantia Fowkes
#cfowkes0@cnet.com
#atlet
#Alphard Ianne
#aianne1@blog.com

def show_list_kualifikasi(request):
    
    data = query("""SELECT * FROM ujian_kualifikasi""")
    role = get_session_data(request)['role']

    context = {
        'data': data,
        'role': role,
        'error': '',
    }
    
    return render(request, "list_kualifikasi.html", context)

def show_form_kualifikasi(request):
    if checkRoleRedirect(request, 'umpire') != 'umpire':
        return redirect(checkRoleRedirect(request, 'umpire'))
    
    if request.method == 'POST':
        tahun = request.POST.get('tahun')
        if not tahun.isdigit():
            context = {
                'error': 'Tahun harus berupa angka'
            }
            return render(request, "form_kualifikasi.html", context)
        batch = request.POST.get('nomor_batch')
        if not batch.isdigit():
            context = {
                'error': 'Batch harus berupa angka'
            }
            return render(request, "form_kualifikasi.html", context)
        tempat_pelaksanaan = request.POST.get('tempat_pelaksanaan')
        tanggal_pelaksanaan = request.POST.get('tanggal_pelaksanaan')
        result = query(f"""INSERT INTO ujian_kualifikasi (tahun, batch, tempat, tanggal) VALUES ({tahun}, {batch}, '{tempat_pelaksanaan}', '{tanggal_pelaksanaan}')""")
        print(result)
        return redirect("/tes_kualifikasi")
    context = {
        'error': ''
    }
    return render(request, "form_kualifikasi.html", context)

def show_pertanyaan_kualifikasi(request,tahun,batch,tempat,tanggal):
    if checkRoleRedirect(request, 'atlet') != 'atlet':
        return redirect(checkRoleRedirect(request, 'atlet'))
    ujianCheck = query(f"""SELECT * FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI WHERE id_atlet = '{get_session_data(request)['id']}' AND tahun = '{tahun}' AND batch = '{batch}' AND tempat = '{tempat}' AND tanggal = '{tanggal}'""")
    print(ujianCheck)
    if ujianCheck != []:
        data = query("""SELECT * FROM ujian_kualifikasi""")
        role = get_session_data(request)['role']
        context = {
            'error': 'Anda sudah pernah mengikuti ujian kualifikasi',
            'data': data,
            'role': role,
        }
        return redirect("/tes_kualifikasi")
    
    if request.method == 'POST':
        question1 = request.POST.get('question1')
        question2 = request.POST.get('question2')
        question3 = request.POST.get('question3')
        question7 = request.POST.get('question7')
        question8 = request.POST.get('question8')
        total = 0
        if(question1 == 'choice1'):
            total += 1
        if(question2 == 'choice1'):
            total += 1
        if(question3 == 'choice1'):
            total += 1
        if(question7 == 'choice1'):
            total += 1
        if(question8 == 'choice1'):
            total += 1

        hasil = False
        if total >= 4:
            hasil = True
        else:
            hasil = False
        insert = query("""
            CREATE OR REPLACE FUNCTION check_ujian_kualifikasi()
            RETURNS TRIGGER AS
            $$
                DECLARE
                    jumlah_ujian integer;
                    world_rank_count integer;
                    world_tour_rank_count integer;
                    minggu integer;
                    bulan integer;
                BEGIN
                    SELECT COUNT(*) INTO jumlah_ujian
                        FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI
                        WHERE id_atlet = NEW.id_atlet AND
                            tahun = NEW.tahun AND
                            batch = NEW.batch AND
                            tempat = NEw.tempat AND
                            tanggal = NEW.tanggal;
                    IF jumlah_ujian > 0 THEN
                        RAISE EXCEPTION 'Atlet sudah pernah mengikuti ujian yang sama';
                    ELSE
                        IF NOT EXISTS (SELECT * FROM ATLET_KUALIFIKASI WHERE ID_Atlet = NEW.id_atlet) THEN
                            IF NEW.Hasil_Lulus = TRUE THEN
                                DELETE FROM ATLET_NON_KUALIFIKASI
                                    WHERE id_atlet = NEW.id_atlet;
                                SELECT MAX(world_rank) INTO world_rank_count FROM ATLET_KUALIFIKASI;
                                SELECT MAX(world_tour_rank) INTO world_tour_rank_count FROM ATLET_KUALIFIKASI;
                                INSERT INTO ATLET_KUALIFIKASI (ID_Atlet, World_Rank,World_Tour_Rank) 
                                    VALUES (NEW.id_atlet, (world_rank_count+1),(world_tour_rank_count+1));
                                SELECT DATE_PART('week',NEW.tanggal) INTO minggu;
                                SELECT DATE_PART('month',NEw.tanggal) INTO bulan;
                                INSERT INTO POINT_HISTORY (ID_Atlet, Minggu_Ke, Bulan, Tahun, Total_Point)
                                    VALUES (NEW.id_atlet, minggu, bulan, NEW.tahun, 50);
                                RETURN NULL;
                            ELSE
                                RETURN NEW;
                            END IF;
                        ELSE
                            RETURN NULL;
                        END IF; 
                        RETURN NULL;
                    END IF;
                END
            $$
            LANGUAGE plpgsql;""")
        print(insert)
        result = query(f"""INSERT INTO atlet_nonkualifikasi_ujian_kualifikasi (id_atlet, tahun, batch, tempat, tanggal, hasil_lulus) VALUES ('{get_session_data(request)['id']}', '{tahun}', '{batch}', '{tempat}', '{tanggal}', {hasil})""")
        print(result)
        return redirect("/tes_kualifikasi/riwayat_kualifikasi")
    return render(request, "pertanyaan_kualifikasi.html")

def show_riwayat_kualifikasi(request):
    data = []
    if get_session_data(request)['role'] == 'umpire':
        data = query(f"""SELECT * FROM atlet_nonkualifikasi_ujian_kualifikasi JOIN member ON atlet_nonkualifikasi_ujian_kualifikasi.id_atlet = member.id""")
        print(data[1][5])
    else:
        data = query(f"""SELECT * FROM atlet_nonkualifikasi_ujian_kualifikasi WHERE id_atlet = '{get_session_data(request)['id']}'""")
    context = {
            'data': data,
            'role': get_session_data(request)['role'],
        }                       
    return render(request, "riwayat_kualifikasi.html", context)