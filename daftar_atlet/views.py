from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from uuid import uuid1

# Create your views here.

# def show_daftar_atlet_umpire(request):
#     return render(request, "daftar_atlet_umpire.html")

# def parse(cursor):
#     columns = [col[0] for col in cursor.description]
#     return [dict(zip(columns, row)) for row in cursor.fetchall()]


def show_list_atlet_umpire(request):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO babadu")
    cursor.execute("SELECT nama, Tgl_Lahir, Negara_Asal, Play_Right, Height, Atlet.World_Rank, World_Tour_Rank, Jenis_Kelamin, SUM(Total_Point) AS Total_Point FROM member, Atlet, Atlet_kualifikasi, point_history WHERE member.id = atlet.id AND atlet.id = atlet_kualifikasi.id_atlet AND atlet_kualifikasi.id_atlet = point_history.id_atlet GROUP BY nama, Tgl_Lahir, Negara_Asal, Play_Right, Height, Atlet.World_Rank, World_Tour_Rank, Jenis_Kelamin;") 
    result = cursor.fetchall()
    list_atlet = []
    for atlet in result:
        jenis_kelamin = "Laki-laki" if atlet[7] else "Perempuan"
        play_right = "Ya" if atlet[3] else "Tidak"
        list_atlet.append({
            "nama" : atlet[0],
            "Tgl_Lahir" : atlet[1],
            "Negara_Asal" : atlet[2],
            "Play_Right" : play_right,
            "Height": atlet[4],
            "World_Rank" : atlet[5],
            "World_Tour_Rank": atlet[6],
            "Jenis_Kelamin" : jenis_kelamin,
            "Total_Point" : atlet[8] 
        })

    cursor2 = connection.cursor()
    cursor2.execute("SET SEARCH_PATH TO babadu")
    cursor2.execute("SELECT nama, Tgl_Lahir, Negara_Asal, Play_Right, Height, Atlet.World_Rank, Jenis_Kelamin FROM member, Atlet, Atlet_non_kualifikasi WHERE member.id = atlet.id AND atlet.id = atlet_non_kualifikasi.id_atlet") 
    result2 = cursor2.fetchall()
    list_atlet2 = []
    for atlet2 in result2:
        jenis_kelamin = "Laki-laki" if atlet2[6] else "Perempuan"
        play_right = "Ya" if atlet2[3] else "Tidak"
        list_atlet2.append({
            "nama" : atlet2[0],
            "Tgl_Lahir" : atlet2[1],
            "Negara_Asal" : atlet2[2],
            "Play_Right" : play_right,
            "Height": atlet2[4],
            "World_Rank" : atlet2[5],
            "Jenis_Kelamin" : jenis_kelamin,
            "Total_point": "0"
        })
    print(list_atlet2)
    cursor3 = connection.cursor()
    cursor3.execute("SET SEARCH_PATH TO babadu")
    cursor3.execute("SELECT ID_Atlet_Ganda, m1.nama as Atlet1, m2.nama as Atlet2, COALESCE((SELECT SUM(p.Total_Point) FROM point_history p WHERE p.id_atlet = m1.id), 0) + COALESCE((SELECT SUM(p.Total_Point) FROM point_history p WHERE p.id_atlet = m2.id), 0) AS Total_Point_ganda FROM atlet_ganda, member m1 JOIN member m2 ON m1.id != m2.id WHERE m1.id = atlet_ganda.ID_Atlet_Kualifikasi AND m2.id = atlet_ganda.ID_Atlet_Kualifikasi_2;") 
    result3 = cursor3.fetchall()
    list_atlet3 = []
    for atlet3 in result3:
        list_atlet3.append({
            "id" : atlet3[0],
            "Nama_Atlet_1" : atlet3[1],
            "Nama_Atlet_2" : atlet3[2],
            "Total_Point" : atlet3[3],
        })
    context = {'data': list_atlet,
                'data2' : list_atlet2,
                'data3' : list_atlet3
    }
                
    # context2 = {'data2': list_atlet2}
    return render(request, "list_atlet_umpire.html",context)

@csrf_exempt
def show_daftar_atlet(request):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO babadu")
    if request.method == 'POST':
        nama_pelatih = request.session['user']['nama']
        id_atlet = request.POST.get("id_atlet")

        # cursor.execute(
        #     f"""
        #     SELECT ID FROM MEMBER WHERE NAMA = 'Windy Kibbe';
        #     """
        # )
        cursor.execute(
            f"""
            SELECT ID FROM MEMBER WHERE NAMA = '{nama_pelatih}';
            """
        )

        id_pelatih = cursor.fetchone()[0]

        if id_atlet:
            # cursor.execute(
            #     f"""
            #     INSERT INTO ATLET_PELATIH VALUES ('6a60a9e8-0941-4649-8f8b-d745856d1da7', '{id_atlet}');
            #     """
            # )
            cursor.execute(
                f"""
                INSERT INTO ATLET_PELATIH VALUES ('{id_pelatih}', '{id_atlet}');
                """
            )

            return redirect("/daftar_atlet/list_atlet/")

    cursor.execute(
        f"""
        SELECT M.Nama, M.id FROM MEMBER M, ATLET A WHERE M.ID=A.ID ORDER BY M.nama;
        """
    )

    result = cursor.fetchall()

    daftar_atlet = []

    for res in result:
        daftar_atlet.append(
            {
                "nama_atlet": res[0],
                "id_atlet": res[1]
            }
        )

    context = {
        "daftar_atlet": daftar_atlet
    }
    return render(request, "daftar_atlet.html", context)

@csrf_exempt
def show_list_atlet(request):
    nama_pelatih = request.session['user']['nama']
    
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO babadu")
    # cursor.execute(
    #     f"""
    #     select id from member m where m.nama = 'Windy Kibbe'
    #     """
    # )
    cursor.execute(
        f"""
        select id from member m where m.nama = '{nama_pelatih}'
        """
    )

    id_pelatih = cursor.fetchone()[0]

    cursor.execute(f"""
                        SELECT MA.Nama, MA.Email, A.World_rank
                        FROM MEMBER MA
                        JOIN ATLET A ON MA.ID = A.ID
                        JOIN ATLET_PELATIH AP ON A.ID = AP.ID_Atlet
                        JOIN PELATIH P ON AP.ID_Pelatih = P.ID
                        """)

    latih_atlet_raw = cursor.fetchall()

    latih_atlet = []

    for res in latih_atlet_raw:
        latih_atlet.append(
            {
                "nama": res[0],
                "email": res[1],
                "world_rank": res[2],
            }
        )
    context = {
        "latih_atlet": latih_atlet
    }
    return render(request, "list_atlet.html", context)


