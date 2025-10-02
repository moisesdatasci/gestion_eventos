from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('eventos/', views.ListaEventosView.as_view(), name='lista_eventos'),
    path('evento/<int:pk>/', views.DetalleEventoView.as_view(), name='detalle_evento'),
    path('evento/crear/', views.CrearEventoView.as_view(), name='crear_evento'),
    path('evento/<int:pk>/editar/', views.EditarEventoView.as_view(), name='editar_evento'),
    path('evento/<int:pk>/eliminar/', views.EliminarEventoView.as_view(), name='eliminar_evento'),
    path('evento/<int:evento_id>/inscribirse/', views.inscribirse_evento, name='inscribirse_evento'),
    path('evento/<int:evento_id>/cancelar/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    path('mis-eventos/', views.mis_eventos, name='mis_eventos'),
    path('acceso-denegado/', views.acceso_denegado, name='acceso_denegado'),
]