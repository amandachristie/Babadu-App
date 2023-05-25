from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from authentication.forms import LoginForm, AtletForm, PelatihForm, UmpireForm

<<<<<<< HEAD
# Create your views here.
from django.shortcuts import render
from utils1.query import query
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
=======
from authentication.query import SQLlogin
from authentication.register import atlet_register, pelatih_register, umpire_register
>>>>>>> ff9d07f223d94a348c27bdcd278704e36b012294


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
            print(request.session['user'])

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
