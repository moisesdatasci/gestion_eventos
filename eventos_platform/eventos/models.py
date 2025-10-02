from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Evento(models.Model):
    TIPO_CHOICES = [
        ('conferencia', 'Conferencia'),
        ('concierto', 'Concierto'),
        ('seminario', 'Seminario'),
        ('taller', 'Taller'),
    ]
    
    PRIVACIDAD_CHOICES = [
        ('publico', 'Público'),
        ('privado', 'Privado'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ubicacion = models.CharField(max_length=300)
    privacidad = models.CharField(max_length=10, choices=PRIVACIDAD_CHOICES, default='publico')
    capacidad = models.PositiveIntegerField(default=50)
    
    # Relación con usuario creador
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_creados')
    
    # Participantes registrados
    participantes = models.ManyToManyField(User, related_name='eventos_inscritos', blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        # Permisos personalizados
        permissions = [
            ('puede_gestionar_eventos', 'Puede gestionar eventos'),
            ('puede_ver_eventos_privados', 'Puede ver eventos privados'),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"
    
    def clean(self):
        if self.fecha_fin and self.fecha_inicio and self.fecha_fin <= self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
    
    def espacios_disponibles(self):
        return self.capacidad - self.participantes.count()
    
    def esta_lleno(self):
        return self.participantes.count() >= self.capacidad