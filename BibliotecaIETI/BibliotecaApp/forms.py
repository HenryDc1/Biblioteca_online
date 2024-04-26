from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django import forms

class ChangePassword(SetPasswordForm):
    old_password = forms.CharField(label='Contrasenya actual', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nova contrasenya', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Repeteix la nova contrasenya', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

         
class Importar(forms.Form):
    csv_file = forms.FileField(label='Arxiu CSV', widget=forms.FileInput(attrs={'class': 'form-control'}))
    centre_educatiu = forms.CharField(label='Nom del centre educatiu', widget=forms.TextInput(attrs={'class': 'form-control'}))

    

class UserProfileForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    cognoms = forms.CharField(label='Surname', widget=forms.TextInput(attrs={'class': 'form-control'}))
    centre = forms.CharField(label='Center', widget=forms.TextInput(attrs={'class': 'form-control'}))
    cicle = forms.CharField(label='Cycle', widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthdate = forms.DateField(label='Birthdate', widget=forms.DateInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Photo', widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile # Cambia User por UserProfile
        fields = ['email', 'name', 'cognoms', 'centre', 'cicle', 'birthdate', 'photo']