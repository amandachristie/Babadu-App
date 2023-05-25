from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from authentication.forms import LoginForm, AtletForm, PelatihForm, UmpireForm
from utils.query import *
from authentication.query import SQLlogin
from authentication.register import atlet_register, pelatih_register, umpire_register


def main_auth(request):
    return render(request, 'main_auth.html')


def user_login(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')

        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False

        user_login = SQLlogin(nama, email)
        print(user_login)
        if len(user_login) > 0:
            user = user_login[0]
            print('ok')
            if user['role'] == 'atlet':
                request.session['is_atlet'] = True
            if user['role'] == 'pelatih':
                request.session['is_pelatih'] = True
            if user['role'] == 'umpire':
                request.session['is_umpire'] = True

            request.session['user'] = user
            userCheck = query(f"""SELECT * FROM member WHERE email='{email}' and nama='{nama}'""")
            request.session["id"] = str(userCheck[0][0])
            print(request.session["id"])
            request.session["role"] = getrole(nama, email)

            if request.session['is_atlet'] or request.session['is_pelatih'] or request.session['is_umpire']:
                response = HttpResponseRedirect(reverse("dashboard:base"))
                return response

        else:
            messages.info(request, 'Username atau Email salah')

    context = {'login_form': LoginForm()}
    return render(request, 'login.html', context)

def user_register(request):
    if request.method == 'POST':
        if "atlet-register" in request.POST:
            form = AtletForm(request.POST)
            if form.is_valid():
                nama = form.cleaned_data.get('nama')
                email = form.cleaned_data.get('email')
                negara = form.cleaned_data.get('negara')
                tanggal_lahir = form.cleaned_data.get('tanggal_lahir')
                play_right = form.cleaned_data.get('play_right')
                tinggi_badan = form.cleaned_data.get('tinggi_badan')
                jenis_kelamin = form.cleaned_data.get('jenis_kelamin')
                register = atlet_register(nama, email, negara, tanggal_lahir, play_right, tinggi_badan, jenis_kelamin)
                if register['success']:
                    return HttpResponseRedirect(reverse("authentication:user_login"))
                else:
                    messages.info(request,register['message'])
                
        
        elif "pelatih-register" in request.POST:
            form = PelatihForm(request.POST)
            if form.is_valid():
                nama = form.cleaned_data.get('nama')
                email = form.cleaned_data.get('email')
                negara = form.cleaned_data.get('negara')
                kategori = form.cleaned_data.get('kategori')
                tanggal_mulai = form.cleaned_data.get('tanggal_mulai')
                register = pelatih_register(nama, email, negara, kategori, tanggal_mulai)
                if register['success']:
                    return HttpResponseRedirect(reverse("authentication:user_login"))
                else:
                    messages.info(request,register['message'])

        elif "umpire-register" in request.POST:
            form = UmpireForm(request.POST)
            print('x')
            print(form.errors)
            if form.is_valid():
                nama = form.cleaned_data.get('nama')
                email = form.cleaned_data.get('email')
                negara = form.cleaned_data.get('negara')
                kategori = form.cleaned_data.get('kategori')
                tanggal_mulai = form.cleaned_data.get('tanggal_mulai')
                register = umpire_register(nama, email, negara)
                if register['success']:
                    return HttpResponseRedirect(reverse("authentication:user_login"))
                else:
                    messages.info(request,register['message'])

    context = { 
        'atlet_form': AtletForm(),
        'pelatih_form': PelatihForm(),
        'umpire_form': UmpireForm(),
    }
    return render(request, 'register.html', context)

def user_logout(request):
    try:
        user = request.session['user']
        print(user[0])
        request.session['user'] = None
        request.session.clear()
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False
        print('sukses!')
        return HttpResponseRedirect(reverse("authentication:user_login"))
    
    except KeyError:
        messages.info(request, "Belum login")
        print('sukses!')
        request.session.clear()
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False
        return HttpResponseRedirect(reverse("authentication:user_login"))

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
    umpireCheck = query(f"""SELECT * FROM umpire WHERE id='{id[0][0]}'""") 
    pelatihCheck = query(f"""SELECT * FROM pelatih WHERE id='{id[0][0]}'""") 
    atletCheck = query(f"""SELECT * FROM atlet WHERE id='{id[0][0]}'""") 

    if pelatihCheck!=[]:
        return "pelatih"
    if umpireCheck!=[]:
        return "umpire"
    if atletCheck!=[]:
        return "atlet"
    return "none"