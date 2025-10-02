from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroUsuarioForm, LoginForm


def registro_view(request):
    """
    Vista para registro de nuevos usuarios
    """
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido {user.username}.')
            login(request, user)  # Login automático después del registro
            return redirect('inicio')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'accounts/registro.html', {'form': form})


def login_view(request):
    """
    Vista para iniciar sesión
    """
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
                
                # Redirigir a la página que intentaba acceder o al inicio
                next_page = request.GET.get('next', 'inicio')
                return redirect(next_page)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Vista para cerrar sesión
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('inicio')


@login_required
def perfil_view(request):
    """
    Vista del perfil del usuario
    """
    return render(request, 'accounts/perfil.html')