#SQL QUERY
from sqlite3 import InternalError
from uuid import UUID
from django.db import connection

# Fetch function
def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def SQLenrolledEvent(nama):
    no_peserta = find_no_peserta(nama)
    query =  f'''SELECT *
        FROM peserta_mendaftar_event P, event E 
        WHERE P.nama_event = E.nama_event AND P.tahun = E.tahun AND P.nomor_peserta = {no_peserta[0]};
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    return res

def find_id(nama):
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

def find_no_peserta(nama):
    id_atlet = find_id(nama)
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

def delete(nama_atlet, nama_event, tahun_event):
    no_peserta = find_no_peserta(nama_atlet)

    try:
        query = f'''DELETE FROM PESERTA_MENDAFTAR_EVENT
            WHERE nomor_peserta = {no_peserta[0]} AND nama_event = '{nama_event}' AND tahun = '{tahun_event}';
            '''
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        cursor.execute(query)
        connection.commit()
        connection.close()
        
    except InternalError as e:
        error_message = str(e)

    return error_message