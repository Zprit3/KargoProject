# Kargo - Sistema de Reservas para Karting

Este proyecto es un sistema web desarrollado con Django para la gestión de reservas en un centro de karting. Permite a los usuarios registrarse, realizar reservas de pistas, y a los administradores gestionar las reservas, las pistas y los usuarios.

## Características principales

*   Registro y autenticación de usuarios.
*   Gestión de reservas (creación, modificación, visualización).
*   Gestión de pistas (creación, modificación, eliminación).
*   Panel de administración para la gestión completa del sistema.
*   Dashboard con estadísticas de reservas.
*   Interfaz intuitiva y fácil de usar.

## Tecnologías utilizadas

*   [Python](https://www.python.org/)
*   [Django](https://www.djangoproject.com/)
*   [PostgreSQL](https://www.postgresql.org/)
*   [Bootstrap](https://getbootstrap.com/)
*   HTML, CSS, JavaScript

## Dependencias

Las dependencias del proyecto se gestionan con `pip`. Puedes instalarlas usando el archivo `requirements.txt`:

## Instalación

1.  **Clonar el repositorio:**

    ```bash
    git clone https://github.com/Zprit3/KargoProject
    cd KargoProject  # Navega a la carpeta del proyecto
    ```

2.  **Crear un entorno virtual (altamente recomendado):**

    Es una buena práctica crear un entorno virtual aislado para tu proyecto. Esto evita conflictos con otras dependencias de Python que puedas tener instaladas en tu sistema.

    *   **Linux/macOS:**

        ```bash
        python3 -m venv .venv        # Crea el entorno virtual (Python 3)
        source .venv/bin/activate   # Activa el entorno virtual
        ```

    *   **Windows:**

        ```bash
        python -m venv .venv         # Crea el entorno virtual
        .venv\Scripts\activate      # Activa el entorno virtual
        ```

3.  **Instalar las dependencias:**

    Una vez activado el entorno virtual, instala las dependencias del proyecto usando `pip`:

    ```bash
    pip install -r requirements.txt
    ```


4.  **Configurar la base de datos:**

    Este proyecto utiliza PostgreSQL.

    *   **Crear la base de datos:** Utiliza `psql` u otra herramienta de administración de bases de datos para crear una nueva base de datos. Por ejemplo, en `psql`:

        ```sql
        CREATE DATABASE kargo_db;  -- Reemplaza con el nombre que desees
        CREATE USER kargo_user WITH PASSWORD 'tu_contraseña';
        ALTER ROLE kargo_user SET client_encoding TO 'utf8';
        ALTER ROLE kargo_user SET default_transaction_isolation TO 'read committed';
        ALTER ROLE kargo_user SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE kargo_db TO kargo_user;
        ```

    *   **Configurar las credenciales en `KargoProject/settings.py`:**

        Abre el archivo `KargoProject/settings.py` y configura la sección `DATABASES` con las credenciales de tu base de datos:

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',  # O 'django.db.backends.mysql', 'django.db.backends.sqlite3', etc.
                'NAME': 'kargo_db',       # Nombre de la base de datos
                'USER': 'kargo_user',
