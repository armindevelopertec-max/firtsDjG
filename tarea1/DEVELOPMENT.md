# 🛠️ Guía de Flujo de Desarrollo (Developer Workflow)

Esta guía explica cómo trabajar en el proyecto día a día utilizando el entorno de contenedores.

---

## 1. Ciclo de Programación Estándar
Gracias a los **Volumes** (`- .:/app:Z`), el flujo es casi idéntico a programar localmente:

1.  **Editas el código** en tu editor favorito (VS Code, Cursor, Vim, etc.) en tu máquina Fedora.
2.  **Guardas el archivo.**
3.  El servidor de Django dentro del contenedor detecta el cambio automáticamente (**Auto-reload**).
4.  **Refrescas el navegador** en `http://localhost:8000`.

> **No es necesario** reiniciar los contenedores cada vez que cambias un archivo `.py`, `.html` o `.css`.

---

## 2. Flujo de Cambios en la Base de Datos
Cada vez que modifiques el archivo `models.py` o añadas un nuevo modelo:

1.  **Crear archivos de migración:**
    ```bash
    podman exec -it django_app python manage.py makemigrations
    ```
2.  **Aplicar cambios a MariaDB:**
    ```bash
    podman exec -it django_app python manage.py migrate
    ```

---

## 3. Flujo de Dependencias (Nuevos Paquetes)
Si necesitas instalar una nueva librería (ejemplo: `requests`):

1.  Abre el archivo `Dockerfile`.
2.  Modifica la línea: `RUN pip install django mysqlclient requests`.
3.  **Reconstruye la imagen** (obligatorio para que el cambio surta efecto):
    ```bash
    podman compose up --build -d
    ```

---

## 4. Debugging y Herramientas de Inspección

### Ver mensajes de error (Print Debugging)
Si pones un `print()` en tu código, los resultados los verás aquí:
```bash
podman logs -f django_app
```

### Probar código rápidamente (Django Shell)
Si quieres interactuar con tus modelos desde la terminal:
```bash
podman exec -it django_app python manage.py shell
```

### Inspeccionar la DB (MariaDB CLI)
Para verificar que los datos se están guardando correctamente en las tablas:
```bash
podman exec -it db_django mariadb -u django_user -p123456 tarea_django
```

---

## 5. Comparativa de Entornos: Host (Fedora) vs Contenedor

| Acción | En el Host (Fedora) | En el Contenedor (Podman) |
| :--- | :--- | :--- |
| **Ejecución de código** | ❌ No se usa | ✅ Django corre aquí |
| **Instalación de librerías** | ❌ `pip install` (ignorar) | ✅ `Dockerfile` + build |
| **Base de Datos** | ❌ MariaDB no instalada | ✅ MariaDB corriendo (puerto 3306) |
| **Escritura de código** | ✅ Tu editor de texto | ❌ No se edita aquí |
| **Linter / Autocompletado** | ✅ `pyenv` / `venv` (opcional) | ❌ No aplica |

**Nota sobre `pyenv`:** Tu entorno `venv` local ahora es solo para el **Linter** de tu editor. No necesitas activar el entorno local para correr el proyecto; basta con tener Podman iniciado.
