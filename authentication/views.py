from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from utils1.query import query
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse

def checkRoleRedirect(request, expected):
    """
    -Hanya berfungsi untuk user sudah login
    -cek apakah session role sama seperti dengan expected, jika tidak redirect ke dashboard
    -expected: string, role yang diharapkan
    -return: string, redirect url
    """
    if get_session_data(request)['role']!= expected:
        role = get_session_data(request)['role']
        if role == 'pelatih':
            return "/dashboard/pelatih"
        if role == 'umpire':
            return "/dashboard/umpire"
        if role == 'atlet':
            return "/dashboard/atlet"
    return expected

def generateId():
    """
    -generate id untuk user yang baru
    -return: string, id
    """
    id = query("""SELECT uuid_in(md5(random()::text || clock_timestamp()::text)::cstring);""")

    return id[0][0]

def is_authenticated(request):
    try:
        request.session["id"]
        return True
    except KeyError:
        return False

def get_session_data(request):
    if not is_authenticated(request):
        return {}
    try:
        return {"id": request.session["id"], "role": request.session["role"]}
    except:
        return {}
    
def getrole(name, email):
    id = query(f"""SELECT id FROM member WHERE email='{email}' and nama='{name}'""")
    umpireCheck = query(f"""SELECT * FROM umpire WHERE id='{id}'""") 
    pelatihCheck = query(f"""SELECT * FROM pelatih WHERE id='{id}'""") 
    atletCheck = query(f"""SELECT * FROM atlet WHERE id='{id}'""") 

    if pelatihCheck!=[]:
        return "pelatih"
    if umpireCheck!=[]:
        return "umpire"
    if atletCheck!=[]:
        return "atlet"
    return "none"

def logout(request):
    next = request.GET.get('next')
    if not is_authenticated(request):
        return redirect("/")
    
    request.session.flush()
    request.session.clear_expired()

    if next != None and next != "None":
        return redirect(next)
    else:
        return redirect("/")
    
def show_login(request):
    next = request.GET.get('next')
    if is_authenticated(request):
        role = get_session_data(request)['role']
        if role == 'pelatih':
            return redirect("/dashboard/pelatih")
        if role == 'umpire':
            return redirect("/dashboard/umpire")
        if role == 'atlet':
            return redirect("/dashboard/atlet")
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        userCheck = query(f"""SELECT * FROM member WHERE email='{email}' and nama='{name}'""")
        if userCheck!=[] and not is_authenticated(request):
            request.session["id"] = userCheck[0]
            request.session["role"] = getrole(name, email)
            request.session.set_expiry(500)
            request.session.modified = True
            if next != None and next != "None":
                return redirect(next)
            else:
                role = get_session_data(request)['role']
                if role == 'pelatih':
                    return redirect("/dashboard/pelatih")
                if role == 'umpire':
                    return redirect("/dashboard/umpire")
                if role == 'atlet':
                    return redirect("/dashboard/atlet")
        else:
            context = {
                "error": "Silahkan cek kembali input Anda!"
                }
            return render(request, "login.html", context)
    context = {
        "error": ""
        }
    return render(request, "login.html",context)

def show_welcome(request):
    return render(request, "welcome.html")

def show_register(request):
    return render(request, "register.html")

def show_register_atlet(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        play_right = True if request.POST.get('play') == 'Right' else False
        tinggi = request.POST.get('tinggi')
        jenis_kelamin = request.POST.get('jenis_kelamin')

        if request.POST.get('play') == None or request.POST.get('jenis_kelamin') == None:
            print("ININ")
            print(request.POST.get('play'))
            print(request.POST.get('jenis_kelamin'))
            context = {
                "error": "Silahkan cek kembali input Anda!"
                }
            return render(request, "register_atlet.html", context)
        

        emailCheck = query(f"""SELECT * FROM member WHERE email='{email}'""")
        if emailCheck==[]:
            id = generateId()
            query(f"""INSERT INTO member (id, nama, email) VALUES ('{id}', '{name}', '{email}')""")
            query(f"""INSERT INTO atlet (id, tgl_lahir, negara_asal, play_right, height, jenis_kelamin) VALUES ('{id}', '{tanggal_lahir}', '{negara}', '{play_right}', '{tinggi}', '{jenis_kelamin}')""")
            return redirect("/login/")
        
        context = {
            "error": "Email sudah terdaftar"
            }
        return render(request, "register_atlet.html", context)

    context = {
        "error": ""
        }
    return render(request, "register_atlet.html", context)

def show_register_umpire(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        negara = request.POST.get('negara')

        emailCheck = query(f"""SELECT * FROM member WHERE email='{email}'""")
        if emailCheck==[]:
            id = generateId()
            query(f"""INSERT INTO member (id, nama, email) VALUES ('{id}', '{name}', '{email}')""")
            query(f"""INSERT INTO umpire (id, negara) VALUES ('{id}', '{negara}')""")
            return redirect("/login/")
        
        context = {
            "error": "Email sudah terdaftar"
            }
        return render(request, "register_umpire.html", context)
    
    context = {
        "error": ""
        }
    
    return render(request, "register_umpire.html")

# id spesialisasi
tunggal_putra = "0692c82c-ba2c-44df-9b93-4e0c7ff1e154"
tunggal_putri = "633c7047-eb93-4809-a573-8e390341b5ea"
ganda_putra = "3eef3282-9fef-45cc-9221-5d0e077f414b"
ganda_putri = "2fc1ffce-41a9-437a-8a93-c550570ff58a"
ganda_campuran = "8a8ec091-d452-477f-9f58-3d9511b0c578"

def show_register_pelatih(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_mulai = request.POST.get('tanggal_mulai')

        emailCheck = query(f"""SELECT * FROM member WHERE email='{email}'""")
        if emailCheck==[]:
            id = generateId()
            query(f"""INSERT INTO member (id, nama, email) VALUES ('{id}', '{name}', '{email}')""")
            query(f"""INSERT INTO pelatih (id, tanggal_mulai) VALUES ('{id}', '{tanggal_mulai}')""")
            if request.POST.get('tunggal-putra') == True:
                query(f"""INSERT INTO PELATIH_SPESIALISASI  (id_pelatih, id_spesialisasi) VALUES ('{id}', '{tunggal_putra}')""")
            if request.POST.get('tunggal-putri') == True:
                query(f"""INSERT INTO PELATIH_SPESIALISASI  (id_pelatih, id_spesialisasi) VALUES ('{id}', '{tunggal_putri}')""")
            if request.POST.get('ganda-putra') == True:
                query(f"""INSERT INTO PELATIH_SPESIALISASI  (id_pelatih, id_spesialisasi) VALUES ('{id}', '{ganda_putra}')""")
            if request.POST.get('ganda-putri') == True:
                query(f"""INSERT INTO PELATIH_SPESIALISASI  (id_pelatih, id_spesialisasi) VALUES ('{id}', '{ganda_putri}')""")
            if request.POST.get('ganda-campuran') == True:
                query(f"""INSERT INTO PELATIH_SPESIALISASI  (id_pelatih, id_spesialisasi) VALUES ('{id}', '{ganda_campuran}')""")
            return redirect("/login/")
        
        context = {
            "error": "Email sudah terdaftar"
            }
        return render(request, "register_pelatih.html", context)
    context = {
        "error": ""
        }
    return render(request, "register_pelatih.html",context)