from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Evento
from accounts.models import PerfilUsuario


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'


class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_rol', 'is_staff']
    
    def get_rol(self, obj):
        return obj.perfil.get_rol_display()
    get_rol.short_description = 'Rol'


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'fecha_inicio', 'ubicacion', 'privacidad', 'creador', 'contar_participantes', 'espacios_disponibles']
    list_filter = ['tipo', 'privacidad', 'fecha_inicio']
    search_fields = ['titulo', 'descripcion', 'ubicacion', 'creador__username']
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'tipo')
        }),
        ('Fechas y Ubicación', {
            'fields': ('fecha_inicio', 'fecha_fin', 'ubicacion')
        }),
        ('Configuración', {
            'fields': ('privacidad', 'capacidad', 'creador')
        }),
        ('Participantes', {
            'fields': ('participantes',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['participantes']
    
    def contar_participantes(self, obj):
        return obj.participantes.count()
    contar_participantes.short_description = 'Participantes'
    
    def espacios_disponibles(self, obj):
        return obj.espacios_disponibles()
    espacios_disponibles.short_description = 'Espacios'


# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)