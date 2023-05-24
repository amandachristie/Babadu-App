#SQL QUERY
from uuid import UUID
from django.db import connection

# Fetch function
def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def sql_enrolled_partai_kompetisi_event(nama):
    no_peserta = find_no_peserta(nama)
    query =  f'''SELECT
                    E.Nama_Event,
                    E.Tahun,
                    E.Nama_Stadium,
                    PK.Jenis_Partai,
                    E.Kategori_Superseries,
                    E.Tgl_Mulai,
                    E.Tgl_Selesai
                FROM
                    PARTAI_PESERTA_KOMPETISI PK, EVENT E 
                WHERE
                    PK.Nama_Event = E.Nama_Event AND PK.Tahun_Event = E.Tahun AND PK.nomor_peserta = {no_peserta[0]};
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
