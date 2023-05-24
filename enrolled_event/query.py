#SQL QUERY
from uuid import UUID
from django.db import connection

# Fetch function
def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def SQLenrolledEvent(nama):
    no_peserta = findNoPeserta(nama)
    query =  f'''SELECT *
        FROM peserta_mendaftar_event P, event E 
        WHERE P.nama_event = E.nama_event AND P.tahun = E.tahun AND P.nomor_peserta = {no_peserta[0]};
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    return res

def findId(nama):
    query =  f'''SELECT ID
        FROM MEMBER
        WHERE Nama = '{nama}';
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    id_atlet = cursor.fetchall()
    print(id_atlet)
    return id_atlet[0]

def findNoPeserta(nama):
    id_atlet = findId(nama)
    print(id_atlet)
    query =  f'''SELECT nomor_peserta
        FROM PESERTA_KOMPETISI
        WHERE id_atlet_kualifikasi = '{id_atlet[0]}';
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    no_peserta = cursor.fetchall()
    return no_peserta[0]
