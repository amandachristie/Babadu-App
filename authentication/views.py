from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from authentication.forms import LoginForm, AtletForm, PelatihForm, UmpireForm
from authentication.query import *
from django.shortcuts import render

#Create your views here
def welcome(request):
    return render(request, 'welcome.html')

def login(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')

        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False

        user_login = execute_login(nama, email)
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
            print(request.session['user'])

            if request.session['is_atlet'] or request.session['is_pelatih'] or request.session['is_umpire']:
                response = HttpResponseRedirect(reverse("dashboard:base"))
                return response

        else:
            messages.info(request, 'Username atau Email salah')

    context = {'login_form': LoginForm()}
    return render(request, 'login.html', context)

def register(request):
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
            if form.is_valid():
                nama = form.cleaned_data.get('nama')
                email = form.cleaned_data.get('email')
                negara = form.cleaned_data.get('negara')
                kategori = form.cleaned_data.get('kategori')
                tanggal_mulai = form.cleaned_data.get('tanggal_mulai')
                register = umpire_register(nama, email, negara)
                if register['success']:
                    return HttpResponseRedirect(reverse("authentication:login"))
                else:
                    messages.info(request,register['message'])

    return render(request, 'register.html', {'atlet_form': AtletForm(), 'pelatih_form': PelatihForm(), 'umpire_form': UmpireForm(),})

def logout(request):
    try:
        user = request.session['user']
        request.session['user'] = None
        request.session.clear()
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False
        print('sukses!')
        return HttpResponseRedirect(reverse("authentication:login"))
    
    except KeyError:
        messages.info(request, "Belum login")
        request.session.clear()
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False
        return HttpResponseRedirect(reverse("authentication:login"))
