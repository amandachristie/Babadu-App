from http.client import HTTPMessage
from django.http import HttpResponseForbidden
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db import connection
from collections import namedtuple
from utils.query import query

# Create your views here.
def show_daftar_stadium(request):
    stadium_fetch = query(f"""
        SELECT EVENT.nama_stadium, EVENT.negara, STADIUM.kapasitas
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
                    "kapasitas": res[4]
                }
            )

        context = {
            "event": event
        }
        print(context)

        return render(request, "daftar_event.html", {"context" : context})


def show_daftar_kategori(request):
    return render(request, "daftar_kategori.html")