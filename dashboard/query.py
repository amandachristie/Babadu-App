#SQL QUERY
from django.db import connection

# Fetch function
def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def SQLprofileAtlet(nama):
    query =  f'''SELECT *
        FROM MEMBER M, ATLET A
        WHERE M.nama = '{nama}' AND M.id = A.id;
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    return res

def SQLprofilePelatih(nama):
    query =  f'''SELECT *
        FROM MEMBER M, PELATIH P
        WHERE M.nama = '{nama}' AND M.id = P.id;
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    return res

def SQLprofileUmpire(nama):
    query =  f'''SELECT *
        FROM MEMBER M, UMPIRE U
        
        WHERE M.nama = '{nama}' AND M.id = U.id;
        '''
             
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    return res