from django import forms
from django.forms import Form


class LoginForm(Form):
    nama = forms.CharField(label='nama', widget=forms.TextInput(
        attrs={'id': 'login-nama', 'placeholder': 'Name'}))
    email = forms.CharField(label='email', widget=forms.EmailInput(
        attrs={'id': 'login-email', 'placeholder': 'Email'}))


class AtletForm(Form):
    nama = forms.CharField(label='nama', widget=forms.TextInput(
        attrs={'id': 'register-nama', 'placeholder': 'Name'}))
    email = forms.CharField(label='email', widget=forms.EmailInput(
        attrs={'id': 'register-email', 'placeholder': 'Email'}))
    negara = forms.CharField(label='negara', widget=forms.TextInput(
        attrs={'id': 'register-negara', 'placeholder': 'Negara'}))
    tanggal_lahir = forms.DateField(label='tanggal-lahir', widget=forms.DateInput(
        attrs={'type': 'date'}))
    play_right = forms.ChoiceField(label='play-right',
                                   choices=[
                                       (True, 'Right Hand'),
                                       (False, 'Left Hand')
                                   ],
                                   widget=forms.RadioSelect(attrs={'class': ''}))
    tinggi_badan = forms.IntegerField(label='tanggal-lahir', widget=forms.NumberInput(
        attrs={'id': 'register-tinggi-badan', 'placeholder': 'Tinggi Badan'}))
    jenis_kelamin = forms.CharField(label='jenis-kelamin', widget=forms.RadioSelect(
        choices=[
            (True, 'Laki-laki'),
            (False, 'Perempuan')
        ]))


class PelatihForm(Form):
    nama = forms.CharField(label='nama', widget=forms.TextInput(
        attrs={'id': 'register-nama', 'placeholder': 'Name'}))
    email = forms.CharField(label='email', widget=forms.EmailInput(
        attrs={'id': 'register-email', 'placeholder': 'Email'}))
    negara = forms.CharField(label='negara', widget=forms.TextInput(
        attrs={'id': 'register-negara', 'placeholder': 'Negara'}))
    kategori = forms.MultipleChoiceField(
        label='kategori',
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ('Tunggal Putra', 'Tunggal Putra'),
            ('Tunggal Putri', 'Tunggal Putri'),
            ('Ganda Putra', 'Ganda Putra'),
            ('Ganda Putri', 'Ganda Putri'),
            ('Ganda campuran', 'Ganda campuran')
        ])
    tanggal_mulai = forms.DateField(label='tanggal-mulai', widget=forms.DateInput(
        attrs={'type': 'date'}))


class UmpireForm(Form):
    nama = forms.CharField(label='nama', widget=forms.TextInput(
        attrs={'id': 'register-nama', 'placeholder': 'Name'}))
    email = forms.CharField(label='email', widget=forms.EmailInput(
        attrs={'id': 'register-email', 'placeholder': 'Email'}))
    negara = forms.CharField(label='negara', widget=forms.TextInput(
        attrs={'id': 'register-negara', 'placeholder': 'Negara'}))