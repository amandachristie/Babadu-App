from django.db import DatabaseError, IntegrityError, transaction
from collections import namedtuple
import psycopg2
from psycopg2 import Error

try:

    connection = psycopg2.connect(user="postgres",
                                  password="BFNIsd1re9Iamm7uyeb9",
                                  host="containers-us-west-39.railway.app",
                                  port="7733",
                                  database="railway")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
        
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def query(query_str: str):
    hasil = []
    # tmp = connection.cursor()
    with connection.cursor() as cursor:
        try:
            cursor.execute("SET search_path TO babadu")
        except Exception as e:
            hasil = e
            connection.rollback()
            # cursor = tmp

        try:
            cursor.execute(query_str)
            if query_str.strip().lower().startswith("select"):
                # Kalau ga error, return hasil SELECT
                hasil = map_cursor(cursor)
            else:
                # Kalau ga error, return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE
                hasil = cursor.rowcount
                # Buat commit di database
                connection.commit()
        except Exception as e:
            # Ga tau error apa
            hasil = e
            connection.rollback()

    return hasil
