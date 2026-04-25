# 🚀 Proyecto Django + MariaDB (Docker/Podman)

Este proyecto ha sido migrado a una arquitectura de contenedores para garantizar la compatibilidad total con **MariaDB** y evitar conflictos de dependencias locales en Fedora (como `mysqlclient`).

---

## 🏗️ Arquitectura del Proyecto

- **Contenedor `django_app`**: Ejecuta Django 6.0 sobre Python 3.12.
- **Contenedor `db_django`**: Base de datos MariaDB 10.11.
- **Red interna**: Los contenedores se comunican a través de una red privada (`django_net`).

---

## 🕹️ Guía de Operación (Comandos Rápidos)

### 1. Levantar el entorno
Para iniciar el proyecto por primera vez o después de cambios en el `Dockerfile`:
```bash
podman compose up --build -d
```

### 2. Detener el entorno
```bash
podman compose down
```

### 3. Ver logs en tiempo real
Si algo falla o quieres ver las peticiones HTTP que llegan:
```bash
podman logs -f django_app
```

---

## 💾 Interacción con la Base de Datos y Django

Al estar en contenedores, ya no ejecutas los comandos directamente en tu terminal, sino **dentro** del contenedor.

### A. Realizar Migraciones
Cuando cambies el archivo `models.py`:
```bash
podman exec -it django_app python manage.py makemigrations
podman exec -it django_app python manage.py migrate
```

### B. Entrar a la consola de MariaDB (CLI)
Para ver las tablas y datos directamente en MariaDB:
```bash
podman exec -it db_django mariadb -u django_user -p123456 tarea_django
```
*Dentro puedes usar: `SHOW TABLES;` o `SELECT * FROM operacion_operacion;`*

### C. Entrar al Shell de Django
```bash
podman exec -it django_app python manage.py shell
```

---

## ❓ Preguntas Frecuentes y Flujo de Trabajo

### 1. ¿Sigo dependiendo de `pyenv` o del `venv` local?
**No.** Ahora tu "computadora" de desarrollo es el contenedor. 
- `pip list` en tu terminal local mostrará tus librerías de Fedora.
- `podman exec django_app pip list` mostrará las librerías reales que usa el proyecto.
- **Dato útil:** Puedes borrar el `venv` local si quieres ahorrar espacio, ya que Django corre dentro de la imagen Docker. El `venv` local ahora solo sirve para que tu editor de código (VS Code/PyCharm) no marque errores de "import no encontrado".

### 2. ¿Cómo instalo nuevas librerías?
Si necesitas una nueva librería (ej: `pandas`):
1. Añádela al `Dockerfile` en la línea de `RUN pip install ...`.
2. Reconstruye el contenedor: `podman compose up --build -d`.

### 3. ¿Por qué usamos `:Z` en los volúmenes?
En Fedora, **SELinux** protege tu sistema de archivos. El sufijo `:Z` le otorga permiso al contenedor para escribir y leer en tu carpeta actual sin comprometer la seguridad global del sistema.

### 4. ¿Dónde están mis archivos?
Gracias a los `volumes` en `docker-compose.yml`, cualquier cambio que hagas en el código en tu editor (fuera del contenedor) se refleja instantáneamente dentro de `django_app`. **No necesitas reiniciar el contenedor para ver cambios en el código Python.**

---

## 🛠️ Estructura de la Base de Datos (Modelo Operacion)
La tabla `operacion_operacion` guarda:
- `id`: Autoincremental.
- `numero1`: Primer operando (Float).
- `numero2`: Segundo operando (Float).
- `resultado`: Suma de ambos (Float).
- `fecha`: Marca de tiempo automática.
