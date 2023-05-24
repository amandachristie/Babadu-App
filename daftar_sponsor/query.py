#SQL QUERY
from uuid import UUID
from django.db import connection

# Fetch function
def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def sql_daftar_sponsor(nama_atlet, nama_sponsor, tgl_mulai, tgl_selesai):
    id_atlet = find_id_atlet(nama_atlet)
    id_sponsor = find_id_sponsor(nama_sponsor)
    
    query =  '''INSERT INTO ATLET_SPONSOR (id_atlet, id_sponsor, tgl_mulai, tgl_selesai)
        VALUES (%s, %s, %s, %s);
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query, (id_atlet, id_sponsor, tgl_mulai, tgl_selesai))

    connection.commit()
    connection.close()

def sql_daftar_sponsor_available(nama):
    id_atlet = find_id_atlet(nama)
    query = f'''SELECT nama_brand
        FROM SPONSOR
        WHERE ID NOT IN (
            SELECT ID_Sponsor
            FROM ATLET_SPONSOR
            WHERE ID_Atlet = '{id_atlet[0]}'
        );
        '''
    
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    return res
    
def sql_list_sponsor(nama):
    id_atlet = find_id_atlet(nama)
    query =  f'''SELECT
            SPONSOR.Nama_Brand AS Nama_Sponsor,
            ATLET_SPONSOR.Tgl_Mulai,
            ATLET_SPONSOR.Tgl_Selesai
        FROM SPONSOR
            INNER JOIN ATLET_SPONSOR ON SPONSOR.ID = ATLET_SPONSOR.ID_Sponsor
            INNER JOIN ATLET ON ATLET_SPONSOR.ID_Atlet = ATLET.ID
        WHERE
            ATLET.ID = '{id_atlet[0]}';
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    return res

def find_id_atlet(nama):
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

def find_id_sponsor(nama_brand):
    query =  f'''SELECT id
        FROM SPONSOR
        WHERE nama_brand = '{nama_brand}';
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    id_sponsor = cursor.fetchall()
    print(id_sponsor)
    return id_sponsor[0]

def delete():
    query =  f'''DELETE FROM PESERTA_MENDAFTAR_EVENT
        WHERE nomor_peserta = 5 AND nama_event = 'French Open' AND tahun = '2022';
    '''
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    