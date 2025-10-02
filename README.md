# 🎫 Plataforma de Gestión de Eventos con Autenticación

Sistema completo de gestión de eventos desarrollado con Django que implementa autenticación, autorización basada en roles y control de acceso a eventos públicos y privados. Proyecto académico que demuestra el uso del modelo Auth de Django, mixins de permisos y gestión de usuarios.

## 🎯 Objetivo del Proyecto

Desarrollar una plataforma donde los usuarios puedan registrarse con diferentes roles (Administrador, Organizador, Asistente) y gestionar eventos con control de acceso basado en permisos. El sistema implementa autenticación completa, autorización por roles y protección de recursos según el nivel de acceso.

## ✨ Características Principales

### 🔐 Sistema de Autenticación
- ✅ Registro de usuarios con asignación automática de roles
- ✅ Inicio de sesión con validación
- ✅ Cierre de sesión seguro
- ✅ Redirección automática después de login/logout
- ✅ Protección de vistas con `@login_required`

### 👥 Sistema de Roles y Permisos
- **Administrador:**
  - Acceso completo al sistema
  - Crear, editar y eliminar eventos
  - Ver todos los eventos (públicos y privados)
  - Acceso al panel de administración
  
- **Organizador:**
  - Crear y gestionar eventos propios
  - Editar eventos creados por ellos
  - Ver todos los eventos
  - NO puede eliminar eventos
  
- **Asistente:**
  - Ver eventos públicos
  - Inscribirse en eventos
  - Ver eventos donde está inscrito
  - NO puede crear ni editar eventos

### 🎪 Gestión de Eventos
- ✅ Eventos públicos y privados
- ✅ Control de capacidad de participantes
- ✅ Inscripción y cancelación de inscripción
- ✅ Diferentes tipos: Conferencias, Conciertos, Seminarios, Talleres
- ✅ Fechas de inicio y fin
- ✅ Ubicación y descripción

### 🛡️ Control de Acceso
- ✅ `LoginRequiredMixin` para vistas que requieren autenticación
- ✅ `PermissionRequiredMixin` para verificar permisos específicos
- ✅ `UserPassesTestMixin` para validaciones personalizadas
- ✅ Página de "Acceso Denegado" personalizada
- ✅ Mensajes de error informativos

### 🎨 Interfaz de Usuario
- ✅ Diseño responsivo con Bootstrap 5
- ✅ Sistema de mensajes (success, error, warning, info)
- ✅ Iconos de Bootstrap Icons
- ✅ Navbar con información de usuario y rol
- ✅ Indicadores visuales de eventos públicos/privados

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.x, Django 4.x
- **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
- **Base de datos:** SQLite (desarrollo)
- **Autenticación:** Django Auth System
- **Autorización:** Django Permissions & Groups

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/gestion-eventos-django.git
cd gestion-eventos-django
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install django
```

O con requirements.txt:
```bash
pip install -r requirements.txt
```

### 4. Realizar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```
Ingresa:
- Nombre de usuario
- Email (opcional)
- Contraseña

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

### 7. Acceder a la aplicación

- **Aplicación:** http://127.0.0.1:8000/
- **Panel Admin:** http://127.0.0.1:8000/admin/

## 📁 Estructura del Proyecto

```
gestion-eventos-django/
│
├── eventos_platform/          # Configuración del proyecto
│   ├── settings.py            # Configuraciones (AUTH, SECURITY)
│   ├── urls.py                # URLs principales
│   └── wsgi.py
│
├── eventos/                   # App de eventos
│   ├── models.py              # Modelo Evento
│   ├── forms.py               # EventoForm
│   ├── views.py               # Vistas con Mixins
│   ├── urls.py                # URLs de eventos
│   ├── admin.py               # Configuración del admin
│   └── templates/
│       └── eventos/
│           ├── base.html
│           ├── inicio.html
│           ├── lista_eventos.html
│           ├── detalle_evento.html
│           ├── evento_form.html
│           ├── evento_confirmar_eliminacion.html
│           ├── mis_eventos.html
│           └── acceso_denegado.html
│
├── accounts/                  # App de cuentas
│   ├── models.py              # PerfilUsuario
│   ├── forms.py               # RegistroForm, LoginForm
│   ├── views.py               # Login, Registro, Logout
│   ├── urls.py                # URLs de autenticación
│   ├── admin.py
│   └── templates/
│       └── accounts/
│           ├── login.html
│           ├── registro.html
│           └── perfil.html
│
├── db.sqlite3                 # Base de datos
├── manage.py
├── requirements.txt
└── README.md
```

## 🗄️ Modelos de Datos

### Modelo: Evento

```python
- titulo (CharField, 200)
- descripcion (TextField)
- tipo (CharField: conferencia, concierto, seminario, taller)
- fecha_inicio (DateTimeField)
- fecha_fin (DateTimeField)
- ubicacion (CharField, 300)
- privacidad (CharField: publico, privado)
- capacidad (PositiveIntegerField)
- creador (ForeignKey → User)
- participantes (ManyToManyField → User)
- fecha_creacion (DateTimeField, auto)
- fecha_actualizacion (DateTimeField, auto)
```

**Permisos Personalizados:**
- `puede_gestionar_eventos`
- `puede_ver_eventos_privados`

### Modelo: PerfilUsuario

```python
- user (OneToOneField → User)
- rol (CharField: asistente, organizador, administrador)
- telefono (CharField, opcional)
- biografia (TextField, opcional)
```

**Señales:** Crea automáticamente el perfil al crear un usuario.

## 🔑 Sistema de Autenticación

### Configuración en settings.py

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'inicio'

# Seguridad
SESSION_COOKIE_SECURE = False  # True en producción
CSRF_COOKIE_SECURE = False     # True en producción
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 hora
```

### Flujo de Autenticación

1. **Registro:**
   - Usuario completa formulario con rol
   - Sistema crea usuario y perfil
   - Asigna permisos según rol automáticamente
   - Login automático después del registro

2. **Login:**
   - Validación de credenciales
   - Redirección a página solicitada o inicio
   - Mensaje de bienvenida

3. **Logout:**
   - Cierre de sesión
   - Mensaje informativo
   - Redirección al inicio

## 🛡️ Mixins de Autenticación Implementados

### LoginRequiredMixin
```python
class CrearEventoView(LoginRequiredMixin, CreateView):
    # Solo usuarios autenticados pueden acceder
    login_url = 'login'
```

### PermissionRequiredMixin
```python
class CrearEventoView(PermissionRequiredMixin, CreateView):
    # Requiere permiso específico
    permission_required = 'eventos.add_evento'
```

### UserPassesTestMixin
```python
class EditarEventoView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        # Prueba personalizada: ¿es el creador?
        evento = self.get_object()
        return self.request.user == evento.creador
```

## 📊 Grupos y Permisos

### Grupos Automáticos

El sistema crea automáticamente 3 grupos:

1. **Administradores**
   - Todos los permisos sobre Evento
   - `is_staff = True`

2. **Organizadores**
   - `add_evento`
   - `change_evento`
   - `view_evento`
   - `puede_gestionar_eventos`

3. **Asistentes**
   - `view_evento`

### Asignación Automática de Permisos

Los permisos se asignan automáticamente al registrarse según el rol elegido. Esto se maneja en el método `asignar_permisos_por_rol()` del formulario de registro.

## 🌐 Rutas de la Aplicación

### Rutas Públicas (Sin autenticación)

| URL | Vista | Descripción |
|-----|-------|-------------|
| `/` | inicio | Página principal |
| `/accounts/registro/` | registro_view | Registro de usuarios |
| `/accounts/login/` | login_view | Iniciar sesión |
| `/eventos/` | ListaEventosView | Lista de eventos públicos |

### Rutas Protegidas (Requieren login)

| URL | Vista | Permisos |
|-----|-------|----------|
| `/accounts/logout/` | logout_view | Autenticado |
| `/accounts/perfil/` | perfil_view | Autenticado |
| `/mis-eventos/` | mis_eventos | Autenticado |
| `/evento/<id>/inscribirse/` | inscribirse_evento | Autenticado |
| `/evento/<id>/cancelar/` | cancelar_inscripcion | Autenticado |

### Rutas con Permisos Especiales

| URL | Vista | Permisos Requeridos |
|-----|-------|---------------------|
| `/evento/crear/` | CrearEventoView | `add_evento` (Org/Admin) |
| `/evento/<id>/editar/` | EditarEventoView | `change_evento` + ser creador |
| `/evento/<id>/eliminar/` | EliminarEventoView | `delete_evento` (Solo Admin) |
| `/evento/<id>/` | DetalleEventoView | Depende si es público/privado |

## 💻 Uso de la Aplicación

### Registrarse

1. Clic en "Registrarse" en el navbar
2. Completar formulario:
   - Nombre de usuario (único)
   - Nombre y apellido
   - Email
   - Rol (Asistente, Organizador, Administrador)
   - Contraseña (2 veces)
3. Sistema asigna permisos automáticamente
4. Login automático

### Crear un Evento (Organizador/Admin)

1. Clic en "Crear Evento"
2. Completar formulario:
   - Título
   - Descripción
   - Tipo de evento
   - Fechas (inicio y fin)
   - Ubicación
   - Privacidad (público/privado)
   - Capacidad
3. Guardar → El usuario actual es el creador

### Inscribirse a un Evento (Cualquier usuario autenticado)

1. Ver detalles del evento
2. Verificar:
   - Evento no está lleno
   - Tiene acceso (si es privado)
3. Clic en "Inscribirse al Evento"
4. Confirmación con mensaje

### Gestionar Eventos (Según rol)

**Administrador:**
- Puede editar CUALQUIER evento
- Puede eliminar CUALQUIER evento
- Ve todos los eventos (públicos y privados)

**Organizador:**
- Puede editar solo SUS eventos
- NO puede eliminar eventos
- Ve todos los eventos

**Asistente:**
- NO puede editar eventos
- NO puede eliminar eventos
- Ve solo eventos públicos y donde está inscrito

## 🎓 Requisitos Académicos Cumplidos

### ✅ Configuración del Modelo Auth
- Sistema de autenticación configurado
- Login/Logout implementados
- Registro de usuarios funcional
- Protección de vistas con decoradores y mixins

### ✅ Enrutamiento Login/Logout
- URLs `/accounts/login/` y `/accounts/logout/`
- `LOGIN_REDIRECT_URL` configurado
- `LOGOUT_REDIRECT_URL` configurado
- Redirección a página solicitada después de login

### ✅ Gestión de Roles y Permisos
- 3 roles implementados (Admin, Organizador, Asistente)
- Permisos asignados automáticamente
- Control de acceso basado en roles
- Uso del sistema de permisos de Django

### ✅ Uso de Mixins
- `LoginRequiredMixin` en vistas protegidas
- `PermissionRequiredMixin` para permisos específicos
- `UserPassesTestMixin` para validaciones personalizadas
- `handle_no_permission()` implementado

### ✅ Redirección de Accesos No Autorizados
- Página de "Acceso Denegado" personalizada
- Mensajes de error informativos
- Redirección automática según contexto

### ✅ Manejo de Errores y Mensajes
- Sistema de mensajes Django (`messages`)
- Mensajes success, error, warning, info
- Feedback visual inmediato al usuario

### ✅ Migraciones Ejecutadas
- Modelos migrados correctamente
- Tablas en base de datos creadas
- Permisos personalizados registrados

### ✅ Exploración de auth_permission
- Permisos estándar de Django creados
- Permisos personalizados agregados
- Sistema de grupos implementado

### ✅ Configuración de Seguridad
- Sesiones configuradas
- Cookies seguras (preparadas para HTTPS)
- Tiempo de expiración de sesión

## 🧪 Casos de Prueba

### Pruebas de Autenticación

1. **Registro exitoso**
   - Resultado: Usuario creado, login automático, permisos asignados

2. **Login con credenciales correctas**
   - Resultado: Sesión iniciada, redirección correcta

3. **Login con credenciales incorrectas**
   - Resultado: Mensaje de error, permanece en login

4. **Acceso a vista protegida sin login**
   - Resultado: Redirección a login

### Pruebas de Roles

1. **Asistente intenta crear evento**
   - Resultado: Página de acceso denegado

2. **Organizador crea evento**
   - Resultado: Evento creado exitosamente

3. **Organizador intenta editar evento de otro**
   - Resultado: Acceso denegado

4. **Administrador elimina cualquier evento**
   - Resultado: Evento eliminado

### Pruebas de Eventos Privados

1. **Usuario no autenticado intenta ver evento privado**
   - Resultado: Redirección a login

2. **Asistente intenta ver evento privado no inscrito**
   - Resultado: Acceso denegado

3. **Usuario inscrito accede a evento privado**
   - Resultado: Acceso permitido

## 🔍 Exploración de la Base de Datos

### Ver permisos en el shell de Django

```bash
python manage.py shell
```

```python
# Listar permisos de Evento
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from eventos.models import Evento

content_type = ContentType.objects.get_for_model(Evento)
permisos = Permission.objects.filter(content_type=content_type)

for p in permisos:
    print(f"{p.codename} - {p.name}")

# Ver permisos de un usuario
from django.contrib.auth.models import User
user = User.objects.get(username='tu_usuario')
print(f"Rol: {user.perfil.get_rol_display()}")
print(f"Grupos: {[g.name for g in user.groups.all()]}")
print(f"Permisos: {[p.codename for p in user.user_permissions.all()]}")
```

## 📦 Dependencias

```txt
Django>=4.2,<5.0
```

Generar `requirements.txt`:
```bash
pip freeze > requirements.txt
```

## 🔧 Panel de Administración

Accede a `/admin/` con tu superusuario para:

- **Usuarios:**
  - Ver y editar usuarios
  - Ver perfil con rol inline
  - Asignar grupos y permisos manualmente

- **Eventos:**
  - Lista con filtros por tipo, privacidad, fecha
  - Búsqueda por título, descripción, ubicación
  - Contador de participantes
  - Gestión de participantes con `filter_horizontal`

- **Perfiles:**
  - Ver y editar roles de usuarios
  - Información adicional (teléfono, biografía)

## 🤝 Contribuciones

Este es un proyecto académico. Para contribuir:

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 👥 Equipo de Desarrollo

- **[Tu Nombre]** - Desarrollo Full Stack
- **[Compañero 2]** - [Responsabilidad]
- **[Compañero 3]** - [Responsabilidad]

## 📚 Recursos y Documentación

- [Django Authentication System](https://docs.djangoproject.com/en/4.2/topics/auth/)
- [Django Permissions](https://docs.djangoproject.com/en/4.2/topics/auth/default/#permissions-and-authorization)
- [Class-based Views Mixins](https://docs.djangoproject.com/en/4.2/topics/auth/default/#the-loginrequired-mixin)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)

## 📄 Licencia

Este proyecto es de uso académico para el curso de **[Nombre del Curso]** - **[Universidad/Institución]**.

## 📞 Contacto

- 📧 Email: tu-email@ejemplo.com
- 💻 GitHub: [@tu-usuario](https://github.com/tu-usuario)

---

## 🐛 Solución de Problemas

### Error: "No module named 'eventos'"
```bash
# Asegúrate de que la app esté en INSTALLED_APPS
python manage.py check
```

### Error: "Table doesn't exist"
```bash
python manage.py makemigrations
python manage.py migrate
```

### No puedo acceder al admin
```bash
# Crea un superusuario
python manage.py createsuperuser
```

### Los permisos no se asignan al registrarse
- Verifica que el método `asignar_permisos_por_rol()` se ejecute
- Revisa que los grupos existan
- Intenta crear los grupos manualmente desde el admin

### Error 403 Forbidden
- Verifica que `{% csrf_token %}` esté en todos los formularios POST
- Revisa configuración de CSRF en settings.py

---

⭐ **Si este proyecto te fue útil, no olvides darle una estrella en GitHub!**

## 📸 Capturas de Pantalla

_(Agrega capturas de pantalla de tu aplicación)_

1. Página de inicio
2. Formulario de registro con roles
3. Login
4. Lista de eventos con indicadores público/privado
5. Detalle de evento con participantes
6. Página de acceso denegado
7. Panel de administración

---

**Desarrollado con ❤️ usando Django Auth System y Bootstrap 5**
