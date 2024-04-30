from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django import forms
from .models import User


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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'fecha_nacimiento', 'centro', 'ciclo', 'image', 'telefono', 'first_name', 'last_name']