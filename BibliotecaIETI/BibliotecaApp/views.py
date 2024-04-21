from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .forms import ChangePassword
from django.contrib import messages

# Create your views here.
def index(request):
    if request.method == "POST":
        # Validate using the User model
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Aqui deberia ir un mensaje de exito.
            messages.success(request, 'User Ok')
            return redirect('index')
        else:
            # Aqui deberia ir un mensaje de error.
            messages.success(request, 'Email o contrasenya incorrectes')
            return redirect('index')
    else:
        return render(request, 'myapp/index.html', {})
    
    
def logout_user(request):
    logout(request)
    messages.success(request, 'Fins aviat!')
    return redirect('index')

def canviar_contrasenya(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePassword(current_user,request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                current_user.set_password(new_password)
                current_user.save()
                update_session_auth_hash(request, current_user)
                messages.success(request, 'Contraseña cambiada correctamente')
                return redirect('index')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)   
                    return render(request, 'myapp/dashboard/canviar_contrasenya.html', {'form': form})             
        else:
            form = ChangePassword(current_user)
            return render(request, 'myapp/dashboard/canviar_contrasenya.html', {'form': form})
    else:
        messages.error(request, 'No estás autenticat. Inicia sessió per canviar la contrasenya.')
        return redirect('index')

    return render(request, 'myapp/dashboard/canviar_contrasenya.html', {})