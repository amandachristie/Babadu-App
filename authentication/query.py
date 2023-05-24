#SQL QUERY
from django.db import connection

# Fetch function
def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def SQLlogin(nama, email):
    query =  '''SELECT M.nama, M.email,
        CASE
        WHEN A.play_right IS NULL AND P.tanggal_mulai IS NULL
        THEN 'umpire'
        WHEN P.tanggal_mulai IS NOT NULL
        THEN 'pelatih'
        WHEN A.play_right IS NOT NULL
        THEN 'atlet'
        ELSE NULL
        END AS role

        FROM MEMBER M
        FULL OUTER JOIN ATLET A ON M.id = A.id
        FULL OUTER JOIN PELATIH P ON M.id = P.id
        FULL OUTER JOIN UMPIRE U ON M.id = U.id
        
        WHERE M.nama =%s AND M.email =%s;
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query, (nama, email))
    res = parse(cursor)
    return res

def SQLRegisterMember(id, nama, email):
    
    query =  '''INSERT INTO MEMBER (id, nama, email)
        VALUES (%s, %s, %s);
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query, (id, nama, email))

    connection.commit()
    connection.close()


def SQLRegisterAtlet(id, tgl_lahir, negara_asal, play_right, height, world_rank, jenis_kelamin):
    query =  '''INSERT INTO ATLET (id, tgl_lahir, negara_asal, play_right, height, world_rank, jenis_kelamin)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query, (id, tgl_lahir, negara_asal, play_right, height, world_rank, jenis_kelamin))

    connection.commit()
    connection.close()


def SQLRegisterPelatih(id, tanggal_mulai, negara):
    query =  '''INSERT INTO PELATIH (id, tanggal_mulai, negara)
        VALUES (%s, %s, %s);
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query, (id, tanggal_mulai, negara))
    
    connection.commit()
    connection.close()

def SQLRegisterSpesialisasi(id, kategori):
    for item in kategori:
        print(item)
        print(type(item))
        
        query =  f'''INSERT INTO PELATIH_SPESIALISASI (id_pelatih, id_spesialisasi)
            SELECT '{id}', S.id
            FROM SPESIALISASI S
            WHERE S.spesialisasi = '{item}';
            '''
                
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        cursor.execute(query)
    
        connection.commit()
        connection.close()

def SQLRegisterUmpire(id, negara):
    query =  '''INSERT INTO UMPIRE (id, negara)
        VALUES (%s, %s);
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query, (id, negara))
    
    connection.commit()
    connection.close()


