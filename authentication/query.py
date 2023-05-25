from django.db import connection
import uuid
from psycopg2 import InternalError

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def execute_login(nama, email):
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute('''SELECT M.nama, M.email,
                    CASE
                    WHEN A.play_right IS NULL AND P.tanggal_mulai IS NULL THEN 'umpire'
                    WHEN P.tanggal_mulai IS NOT NULL THEN 'pelatih' 
                    WHEN A.play_right IS NOT NULL THEN 'atlet'
                    ELSE NULL
                    END AS role
                    FROM MEMBER M
                    FULL OUTER JOIN ATLET A ON M.id = A.id
                    FULL OUTER JOIN PELATIH P ON M.id = P.id
                    FULL OUTER JOIN UMPIRE U ON M.id = U.id
                    WHERE M.nama =%s AND M.email =%s;''', (nama, email))
    result = parse(cursor)
    return result

def execute_register(id, nama, email):
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute('''INSERT INTO MEMBER (id, nama, email) VALUES (%s, %s, %s);''', (id, nama, email))
    connection.commit()
    connection.close()

def register_atler(id, tgl_lahir, negara_asal, play_right, height, world_rank, jenis_kelamin):  
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute('''INSERT INTO ATLET (id, tgl_lahir, negara_asal, play_right, height, world_rank, jenis_kelamin) VALUES (%s, %s, %s, %s, %s, %s, %s);''', (id, tgl_lahir, negara_asal, play_right, height, world_rank, jenis_kelamin))
    connection.commit()
    connection.close()

def register_pelatih(id, tanggal_mulai, negara):
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute('''INSERT INTO PELATIH (id, tanggal_mulai, negara) VALUES (%s, %s, %s);''', (id, tanggal_mulai, negara))
    connection.commit()
    connection.close()

def register_spesialisasi(id, spesialisasi):
    for s in spesialisasi:
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        cursor.execute(f'''INSERT INTO PELATIH_SPESIALISASI (id_pelatih, id_spesialisasi) SELECT '{id}', S.id
                        FROM SPESIALISASI S WHERE S.spesialisasi = '{s}';''')
        connection.commit()
        connection.close()

def register_uumpire(id, negara):
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute('''INSERT INTO UMPIRE (id, negara) VALUES (%s, %s);''', (id, negara))
    connection.commit()
    connection.close()


def atlet_register(nama, email, negara, tanggal_lahir, play_right, tinggi_badan, jenis_kelamin):
    try:
        id = uuid.uuid4()
        execute_register(id, nama, email)
        register_atler(id, tanggal_lahir, negara, play_right, tinggi_badan, 0, jenis_kelamin)
    except InternalError as e:
        return {'success': False, 'message': str(e.args)}
    else:
        return {'success': True,}
    
def pelatih_register(nama, email, negara, spesialisasi, tanggal_mulai):
    try:
        id = uuid.uuid4()
        execute_register(id, nama, email)
        register_pelatih(id, tanggal_mulai, negara)
        register_spesialisasi(id, spesialisasi)
    except InternalError as e:
        return { 'success': False, 'message': str(e.args)
        }
    else:
        return {
            'success': True,
        }
    
def umpire_register(nama, email, negara):
    try:
        id = uuid.uuid4()
        execute_register(id, nama, email)
        register_uumpire(id, negara)
    except InternalError as e:
        return { 'success': False, 'message': str(e.args)}
    else:
        return {'success': True,}