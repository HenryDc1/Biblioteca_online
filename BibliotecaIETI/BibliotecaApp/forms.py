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

         
        