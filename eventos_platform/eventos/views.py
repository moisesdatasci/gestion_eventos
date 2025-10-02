from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Evento
from .forms import EventoForm


# ========== Vistas basadas en funciones ==========

def inicio(request):
    """
    Página de inicio - muestra eventos públicos
    """
    if request.user.is_authenticated:
        # Usuarios autenticados ven eventos públicos y privados (si tienen permiso)
        if request.user.has_perm('eventos.puede_ver_eventos_privados') or request.user.perfil.rol in ['administrador', 'organizador']:
            eventos = Evento.objects.all()[:6]
        else:
            # Asistentes ven solo públicos y donde están inscritos
            eventos = Evento.objects.filter(
                Q(privacidad='publico') | Q(participantes=request.user)
            ).distinct()[:6]
    else:
        # Usuarios no autenticados solo ven públicos
        eventos = Evento.objects.filter(privacidad='publico')[:6]
    
    return render(request, 'eventos/inicio.html', {'eventos': eventos})


@login_required
def mis_eventos(request):
    """
    Eventos donde el usuario está inscrito
    """
    eventos_inscritos = request.user.eventos_inscritos.all()
    return render(request, 'eventos/mis_eventos.html', {'eventos': eventos_inscritos})


@login_required
def inscribirse_evento(request, evento_id):
    """
    Inscribir al usuario en un evento
    """
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar si el evento es privado y el usuario tiene permiso
    if evento.privacidad == 'privado' and not request.user.has_perm('eventos.puede_ver_eventos_privados'):
        messages.error(request, 'No tienes permiso para acceder a este evento privado.')
        return redirect('acceso_denegado')
    
    # Verificar capacidad
    if evento.esta_lleno():
        messages.warning(request, 'Este evento ha alcanzado su capacidad máxima.')
        return redirect('detalle_evento', pk=evento.id)
    
    # Verificar si ya está inscrito
    if request.user in evento.participantes.all():
        messages.info(request, 'Ya estás inscrito en este evento.')
    else:
        evento.participantes.add(request.user)
        messages.success(request, f'Te has inscrito exitosamente en "{evento.titulo}".')
    
    return redirect('detalle_evento', pk=evento.id)


@login_required
def cancelar_inscripcion(request, evento_id):
    """
    Cancelar inscripción a un evento
    """
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.user in evento.participantes.all():
        evento.participantes.remove(request.user)
        messages.success(request, f'Has cancelado tu inscripción a "{evento.titulo}".')
    else:
        messages.info(request, 'No estabas inscrito en este evento.')
    
    return redirect('mis_eventos')


def acceso_denegado(request):
    """
    Página de acceso denegado
    """
    return render(request, 'eventos/acceso_denegado.html')


# ========== Vistas basadas en clases ==========

class ListaEventosView(ListView):
    """
    Lista de todos los eventos (filtra según permisos)
    """
    model = Evento
    template_name = 'eventos/lista_eventos.html'
    context_object_name = 'eventos'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Evento.objects.all()
        
        if not self.request.user.is_authenticated:
            # Solo eventos públicos para no autenticados
            return queryset.filter(privacidad='publico')
        
        # Administradores y organizadores ven todo
        if self.request.user.perfil.rol in ['administrador', 'organizador']:
            return queryset
        
        # Asistentes ven públicos y donde están inscritos
        return queryset.filter(
            Q(privacidad='publico') | Q(participantes=self.request.user)
        ).distinct()


class DetalleEventoView(DetailView):
    """
    Detalle de un evento
    """
    model = Evento
    template_name = 'eventos/detalle_evento.html'
    context_object_name = 'evento'
    
    def dispatch(self, request, *args, **kwargs):
        evento = self.get_object()
        
        # Verificar acceso a eventos privados
        if evento.privacidad == 'privado':
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para ver este evento.')
                return redirect('login')
            
            # Verificar si tiene permiso o está inscrito
            if not (request.user.has_perm('eventos.puede_ver_eventos_privados') or 
                    request.user in evento.participantes.all() or
                    request.user == evento.creador):
                messages.error(request, 'No tienes permiso para ver este evento privado.')
                return redirect('acceso_denegado')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['esta_inscrito'] = self.request.user in self.object.participantes.all()
            context['es_creador'] = self.request.user == self.object.creador
        return context


class CrearEventoView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Crear un nuevo evento (solo organizadores y administradores)
    """
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('lista_eventos')
    permission_required = 'eventos.add_evento'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para crear eventos.')
        return redirect('acceso_denegado')
    
    def form_valid(self, form):
        form.instance.creador = self.request.user
        messages.success(self.request, f'Evento "{form.instance.titulo}" creado exitosamente.')
        return super().form_valid(form)


class EditarEventoView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Editar un evento (solo creador, organizadores y administradores)
    """
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    permission_required = 'eventos.change_evento'
    
    def test_func(self):
        evento = self.get_object()
        user = self.request.user
        # Solo el creador, organizadores y administradores pueden editar
        return (user == evento.creador or 
                user.perfil.rol in ['administrador', 'organizador'])
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para editar este evento.')
        return redirect('acceso_denegado')
    
    def get_success_url(self):
        messages.success(self.request, 'Evento actualizado exitosamente.')
        return reverse_lazy('detalle_evento', kwargs={'pk': self.object.pk})


class EliminarEventoView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Eliminar un evento (solo administradores)
    """
    model = Evento
    template_name = 'eventos/evento_confirmar_eliminacion.html'
    success_url = reverse_lazy('lista_eventos')
    permission_required = 'eventos.delete_evento'
    
    def test_func(self):
        user = self.request.user
        # Solo administradores pueden eliminar
        return user.perfil.rol == 'administrador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'Solo los administradores pueden eliminar eventos.')
        return redirect('acceso_denegado')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Evento eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)