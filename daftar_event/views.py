from http.client import HTTPMessage
from django.http import HttpResponseForbidden
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db import connection
from collections import namedtuple

from django.urls import reverse
from utils1.query import query
from django.contrib.auth import *

# Create your views here.
def show_daftar_stadium(request):
    stadium_fetch = query(f"""
        SELECT DISTINCT EVENT.nama_stadium, EVENT.negara, STADIUM.kapasitas
        FROM STADIUM, EVENT
        WHERE STADIUM.nama = EVENT.nama_stadium
        """)

    stadium = []

    for res in stadium_fetch:
        stadium.append(
            {
                "nama_stadium": res[0],
                "negara": res[1],
                "kapasitas": res[2],
            }
        )

    context = {
        "stadium": stadium
    }
    print(context)
    return render(request, "daftar_stadium.html", {"context":context})


def show_daftar_event(request, stadium_nama):
        event_fetch = query(f"""
            SELECT EVENT.nama_event, EVENT.total_hadiah, EVENT.tgl_mulai, EVENT.kategori_superseries, STADIUM.kapasitas
            FROM EVENT
            JOIN STADIUM ON STADIUM.nama = EVENT.nama_stadium
            WHERE EVENT.tgl_mulai > CURRENT_DATE AND STADIUM.nama = '{stadium_nama}'
        """)

        event = []

        for res in event_fetch:
            event.append(
                {
                    "nama_event": res[0],
                    "total_hadiah": res[1],
                    "tgl_mulai": res[2],
                    "kategori_superseries": res[3],
                    "kapasitas": res[4],
                    "nama_stadium": stadium_nama,
                }
            )

        context = {
            "event": event
        }
        print(context)

        return render(request, "daftar_event.html", {"context" : context})


def show_daftar_kategori(request, stadium_nama, event_nama):
    event_fetch = query(f"""
            SELECT EVENT.nama_event, EVENT.total_hadiah, EVENT.tgl_mulai, EVENT.tgl_selesai, EVENT.kategori_superseries, STADIUM.kapasitas, EVENT.negara
            FROM EVENT
            JOIN STADIUM ON STADIUM.nama = EVENT.nama_stadium
            WHERE EVENT.tgl_mulai > CURRENT_DATE AND STADIUM.nama = '{stadium_nama}'
        """)
    
    # try:
    #      id = request.session['id']
    # except KeyError:
    #      return redirect(reverse('authentication:show_login'))
    
    # jenis_kelamin = query("SELECT jenis_kelamin FROM BABADU.ATLET WHERE id = {id}")[0]
    
    jenis_kelamin = 1

    if jenis_kelamin == 1:
        md_fetch = query(f"""
                SELECT nomor_peserta 
                FROM PARTAI_PESERTA_KOMPETISI 
                WHERE jenis_partai = 'MD' 
                AND nama_event = '{event_nama}'
            """)
        md = []
        tunggal = "Tunggal Putra"
        ganda = "Ganda Putra"
        for res in md_fetch:
            md.append(
            {
                "nomor_peserta_md": res[0],
                "ganda": ganda,
                "tunggal": tunggal,
            }
        )
        context = {
            "jenis": md,
        }
    else:
        wd_fetch = query(f"""
                SELECT nomor_peserta 
                FROM PARTAI_PESERTA_KOMPETISI 
                WHERE jenis_partai = 'WD' 
                AND nama_event = '{event_nama}'
            """)
        wd = []
        tunggal = "Tunggal Putri"
        ganda = "Ganda Putri"
        for res in wd_fetch:
            wd.append(
            {
                "nomor_peserta_wd": res[0],
                "ganda": ganda,
                "tunggal": tunggal,
            }
        )
        context = {
            "jenis": wd,
        }

    xd_fetch = query(f"""
            SELECT nomor_peserta 
            FROM PARTAI_PESERTA_KOMPETISI 
            WHERE jenis_partai = 'XD' 
            AND nama_event = '{event_nama}'
        """)
    
    campuran = "Ganda Campuran"

    xd = []
    event = {}

    for res in event_fetch:
        event["nama_event"] = res[0]
        event["total_hadiah"] = res[1]
        event["tgl_mulai"] = res[2]
        event["tgl_selesai"] = res[3]
        event["kategori_superseries"] = res[4]
        event["kapasitas"] = res[5]
        event["negara"] = res[6]
        event["nama_stadium"] = stadium_nama
            # event.append(
            #     {
            #         "nama_event": res[0],
            #         "total_hadiah": res[1],
            #         "tgl_mulai": res[2],
            #         "tgl_selesai": res[3],
            #         "kategori_superseries": res[4],
            #         "kapasitas": res[5],
            #         "negara": res[6],
            #         "nama_stadium": stadium_nama,
            #     }
            # )
    
    for res in xd_fetch:
        xd.append(
            {
                "nomor_peserta_xd": res[0],
                # "campuran": campuran,
            }
        )

    context["xd"] = xd,
    context["event"] = event,

    print(context)

    if (request.method == 'POST'):
        kategori = request.POST["kategori"]
        partner = request.POST["partner"]
        print(kategori)
        print(partner)
        query("SET SEARCH_PATH TO BABADU")
        # query(f"""
        #     INSERT INTO 
        # """
        # )

    return render(request, "daftar_kategori.html", {"context" : context})
