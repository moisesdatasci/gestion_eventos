from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario


class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario personalizado para registro de usuarios
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )
    rol = forms.ChoiceField(
        choices=PerfilUsuario.ROL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Actualizar el rol del perfil
            perfil = user.perfil
            perfil.rol = self.cleaned_data['rol']
            perfil.save()
            
            # Asignar permisos según el rol
            self.asignar_permisos_por_rol(user, perfil.rol)
        
        return user
    
    def asignar_permisos_por_rol(self, user, rol):
        """
        Asigna permisos según el rol del usuario
        """
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from eventos.models import Evento
        
        # Limpiar grupos previos
        user.groups.clear()
        
        if rol == 'administrador':
            # Crear o obtener grupo de administradores
            admin_group, created = Group.objects.get_or_create(name='Administradores')
            
            # Dar todos los permisos sobre Evento
            content_type = ContentType.objects.get_for_model(Evento)
            permisos = Permission.objects.filter(content_type=content_type)
            admin_group.permissions.set(permisos)
            
            user.groups.add(admin_group)
            user.is_staff = True  # Acceso al admin de Django
            user.save()
            
        elif rol == 'organizador':
            # Crear o obtener grupo de organizadores
            org_group, created = Group.objects.get_or_create(name='Organizadores')
            
            # Dar permisos específicos
            content_type = ContentType.objects.get_for_model(Evento)
            permisos = Permission.objects.filter(
                content_type=content_type,
                codename__in=['add_evento', 'change_evento', 'view_evento', 'puede_gestionar_eventos']
            )
            org_group.permissions.set(permisos)
            
            user.groups.add(org_group)
            
        else:  # asistente
            # Crear o obtener grupo de asistentes
            asist_group, created = Group.objects.get_or_create(name='Asistentes')
            
            # Solo permiso de ver
            content_type = ContentType.objects.get_for_model(Evento)
            permiso_ver = Permission.objects.filter(
                content_type=content_type,
                codename='view_evento'
            )
            asist_group.permissions.set(permiso_ver)
            
            user.groups.add(asist_group)


class LoginForm(AuthenticationForm):
    """
    Formulario personalizado para login
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )