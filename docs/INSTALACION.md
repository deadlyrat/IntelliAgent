# Guía de instalación

Esta guía lleva a una persona sin experiencia previa desde una máquina limpia hasta IntelliAgent funcionando en `http://localhost:3000`. Cada paso indica el comando y el resultado esperado.

Dos avisos antes de empezar:

- **No hay pruebas automáticas ni CI** en el repositorio. La forma de comprobar que todo funciona es la lista de la sección [Verifica que funciona](#9-verifica-que-funciona).
- **No hay migraciones de base de datos.** Las tablas se crean al arrancar el backend con `SQLModel.metadata.create_all`. Si cambia un modelo después, las tablas existentes no se modifican.

## Contenido

1. [Requisitos y versiones](#1-requisitos-y-versiones)
2. [Obtener el código](#2-obtener-el-código)
3. [Configurar las variables de entorno](#3-configurar-las-variables-de-entorno)
4. [Ejecutar con Docker Compose](#4-ejecutar-con-docker-compose)
5. [Trabajar en desarrollo con Docker](#5-trabajar-en-desarrollo-con-docker)
6. [Ejecutar sin Docker](#6-ejecutar-sin-docker)
7. [Variables de entorno](#7-variables-de-entorno)
8. [Verificar el entorno con check_setup.py](#8-verificar-el-entorno-con-check_setuppy)
9. [Verifica que funciona](#9-verifica-que-funciona)
10. [Solución de problemas](#10-solución-de-problemas)

## 1. Requisitos y versiones

Para la ruta recomendada (Docker Compose) solo se necesitan Git, Docker y una clave de un proveedor de modelos compatible con OpenAI.

| Herramienta | Versión | Para qué | Descarga |
|---|---|---|---|
| Git | cualquiera reciente | Clonar el repositorio | https://git-scm.com/downloads (Windows, macOS y Linux) |
| Docker con Compose v2 | sin versión mínima declarada en el repositorio | Levantar base de datos, backend y frontend | Docker Desktop en Windows y macOS: https://docs.docker.com/desktop/. Docker Engine en Linux: https://docs.docker.com/engine/install/ |
| Clave de API de OpenAI | n/a | El backend no arranca sin `OPENAI_API_KEY` | https://platform.openai.com/api-keys (o la clave de un endpoint compatible) |

Solo para la ruta sin Docker (sección 6):

| Herramienta | Versión | Nota |
|---|---|---|
| Python | 3.13 | Es la versión de la imagen del backend (`python:3.13.4-slim-bullseye`). Descarga: https://www.python.org/downloads/ |
| Node.js | 20 | Es la versión de la imagen que compila el frontend (`node:20-alpine`). Descarga: https://nodejs.org/ |
| PostgreSQL | 17.5 | Puede usar el contenedor de Compose (sección 6.1) |

Comprobar Docker:

```bash
docker --version
docker compose version
```

Resultado esperado: una línea con la versión de cada uno, por ejemplo `Docker version 27.x.x` y `Docker Compose version v2.x.x`. Si `docker compose` no existe pero `docker-compose` sí, es la versión antigua: instale una reciente o sustituya `docker compose` por `docker-compose` en los comandos.

Los comandos de esta guía usan sintaxis de Bash. En Windows funcionan en Git Bash. Donde PowerShell difiere, se indica.

## 2. Obtener el código

```bash
git clone https://github.com/deadlyrat/IntelliAgent.git
cd IntelliAgent
```

Resultado esperado: una carpeta `IntelliAgent` con `backend/`, `frontend/`, `compose.yaml`, `compose.prod.yaml` y `.env.sample` en su raíz.

## 3. Configurar las variables de entorno

Docker Compose lee un archivo `.env` en la raíz del repositorio (`env_file: .env` en `compose.yaml`). Ese archivo no se versiona: el `.gitignore` lo excluye.

El repositorio incluye dos plantillas:

- `.env.example`: lista todas las variables que lee el código, con valores ficticios. Es la plantilla recomendada.
- `.env.sample`: la plantilla original. No incluye `TRELLO_API_KEY`, `TRELLO_API_TOKEN` ni `TRELLO_DEFAULT_LIST_ID`, que el código sí lee.

```bash
cp .env.example .env
```

En PowerShell:

```powershell
Copy-Item .env.example .env
```

Abra `.env` con un editor y reemplace los valores ficticios. Como mínimo hay que definir `API_KEY`, `DATABASE_URL` y `OPENAI_API_KEY`. La tabla completa está en la [sección 7](#7-variables-de-entorno).

Para `DATABASE_URL` con Docker Compose, el host es el nombre del servicio (`db_service`) y el puerto el interno (5432). El usuario, la clave y el nombre de la base deben coincidir con los que `compose.yaml` fija en el servicio `db_service` (variables `POSTGRES_USER`, `POSTGRES_PASSWORD` y `POSTGRES_DB`). Forma de la URL:

```text
postgresql+psycopg://<USUARIO>:<CLAVE>@db_service:5432/<BASE>
```

Use exactamente el prefijo `postgresql+psycopg://`, que selecciona el driver `psycopg` 3 instalado. Con `postgresql://` SQLAlchemy busca el driver `psycopg2`, que no está instalado. Con `postgres://` el código lo reescribe a `postgres+psycopg://` (`backend/src/api/db.py`), pero SQLAlchemy 2 no tiene un dialecto `postgres` y el backend falla al importar.

Nunca suba `.env` al repositorio ni pegue su contenido en un chat o una incidencia.

## 4. Ejecutar con Docker Compose

```bash
docker compose up --build
```

La primera vez descarga imágenes y compila el frontend, lo que puede tardar varios minutos. El orden de arranque es: base de datos (espera a que `pg_isready` responda), backend y frontend.

Resultado esperado al final de los registros del backend:

```text
creating database tables...
INFO:     Application startup complete.
```

Para dejarlo en segundo plano:

```bash
docker compose up --build -d
docker compose ps
```

Resultado esperado: tres contenedores en estado `running` (`intelliagent_db` con estado `healthy`, `intelliagent_backend` e `intelliagent_frontend`).

Puertos publicados en el host por `compose.yaml`:

| Servicio | Contenedor | Puerto en el host | URL |
|---|---|---|---|
| Frontend (Nginx) | `intelliagent_frontend` | 3000 (mapea al 80 del contenedor) | http://localhost:3000 |
| Backend (FastAPI) | `intelliagent_backend` | 8080 (mapea al 8000 del contenedor) | http://localhost:8080 y http://localhost:8080/docs |
| PostgreSQL | `intelliagent_db` | 5433 (mapea al 5432 del contenedor) | `localhost:5433` |

Detener:

```bash
docker compose down
```

Los datos se conservan en el volumen `dc_managed_db_volume`. Para borrarlos también (destruye las investigaciones guardadas):

```bash
docker compose down -v
```

## 5. Trabajar en desarrollo con Docker

`compose.yaml` es la configuración de desarrollo. El backend corre con `uvicorn ... --reload` y monta `./backend/src` dentro del contenedor, así que un cambio en un archivo de Python reinicia el servidor sin reconstruir la imagen. El `CMD` del `backend/Dockerfile` es `python -m http.server 8000`, pero Compose lo sustituye con `command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload`. Si ejecuta la imagen con `docker run` sin indicar un comando, no arranca la API.

El frontend no tiene recarga en caliente en esta configuración: el contenedor sirve con Nginx los archivos ya compilados. Tras cambiar código de `frontend/`, reconstruya solo ese servicio:

```bash
docker compose up --build -d frontend
```

`compose.yaml` también define un bloque `develop.watch` para el backend (reconstruye si cambian `requirements.txt` o el `Dockerfile`, reinicia si cambia `src`). Se activa con:

```bash
docker compose watch
```

## 6. Ejecutar sin Docker

Esta ruta sirve para depurar. Tiene tres particularidades que salen del código:

- El backend no carga `.env` por sí mismo (no usa `python-dotenv`). Las variables deben estar en el entorno del proceso.
- El proxy de desarrollo de Vite apunta a `http://backend:8000` (`frontend/vite.config.js`). Ese nombre solo existe dentro de la red de Compose.
- Hace falta una base PostgreSQL accesible desde `DATABASE_URL`.

### 6.1 Base de datos

La opción más corta es usar solo el contenedor de base de datos de Compose:

```bash
docker compose up -d db_service
```

Resultado esperado: `intelliagent_db` en estado `healthy`. Desde el host la base escucha en `localhost:5433`, así que `DATABASE_URL` es:

```text
postgresql+psycopg://<USUARIO>:<CLAVE>@localhost:5433/<BASE>
```

Si prefiere un PostgreSQL propio, cree una base y un usuario y use su host y puerto.

### 6.2 Backend

Desde la raíz del repositorio:

```bash
cd backend
python -m venv .venv
```

Active el entorno virtual. En Git Bash en Windows: `source .venv/Scripts/activate`. En PowerShell: `.venv\Scripts\Activate.ps1`. En macOS y Linux: `source .venv/bin/activate`.

```bash
pip install -r requirements.txt
```

Exporte las variables (Git Bash, macOS y Linux). Use `set -a` para exportar todo lo que cargue `.env`:

```bash
set -a
source ../.env
set +a
```

Atención: dentro de `.env` el host de `DATABASE_URL` debe ser `localhost:5433` en este modo, no `db_service:5432`. Edite esa línea antes de cargarlo.

En PowerShell hay que definirlas una a una, por ejemplo:

```powershell
$env:API_KEY = "<VALOR>"
$env:OPENAI_API_KEY = "<VALOR>"
$env:DATABASE_URL = "postgresql+psycopg://<USUARIO>:<CLAVE>@localhost:5433/<BASE>"
```

Arrancar el servidor desde `backend/src`:

```bash
cd src
uvicorn main:app --reload --port 8000
```

Resultado esperado:

```text
creating database tables...
INFO:     Application startup complete.
```

El backend queda en http://localhost:8000 (en este modo no hay mapeo 8080).

### 6.3 Frontend

En otra terminal:

```bash
cd frontend
npm install
```

Como el proxy de Vite apunta a `http://backend:8000`, hay dos formas de que `/api` llegue al backend local. Elija una:

- Opción A: editar `target` en `frontend/vite.config.js` a `http://localhost:8000`. No haga commit de ese cambio.
- Opción B: añadir `127.0.0.1 backend` al archivo hosts del sistema (`C:\Windows\System32\drivers\etc\hosts` en Windows, `/etc/hosts` en macOS y Linux).

Luego:

```bash
npm run dev
```

Resultado esperado: Vite informa `Local: http://localhost:3000/`. Abra esa URL.

## 7. Variables de entorno

Nombres tomados del código del backend. Los valores de la columna Ejemplo son ficticios.

| Nombre | Obligatoria | Qué es | Cómo obtenerla | Ejemplo |
|---|---|---|---|---|
| `API_KEY` | Sí | El backend aborta al importar `main.py` si falta. Hoy no se usa para validar peticiones | La define usted: cualquier cadena larga y aleatoria | `cambiar-esto-por-un-valor-largo` |
| `DATABASE_URL` | Sí | Cadena de conexión a PostgreSQL | Compose: `db_service:5432`. Sin Docker: `localhost:5433` | `postgresql+psycopg://usuario:clave@db_service:5432/base` |
| `OPENAI_API_KEY` | Sí | Clave del proveedor del modelo. El backend aborta al importar `llms.py` si falta | Panel de OpenAI, sección API keys | `sk-ejemplo-no-es-real` |
| `OPENAI_MODEL_NAME` | No | Modelo de chat. Por defecto `gpt-4o-mini` | Catálogo de modelos del proveedor | `gpt-4o-mini` |
| `OPENAI_BASE_URL` | No | URL base de un endpoint compatible con OpenAI. Vacío usa el de OpenAI | Documentación del proveedor alternativo | `https://api.ejemplo.com/v1` |
| `EMAIL_ADDRESS` | Solo para correo | Cuenta que envía y lee correos | Su cuenta de Gmail | `usuario@ejemplo.com` |
| `EMAIL_PASSWORD` | Solo para correo | Contraseña de aplicación de Gmail, no la clave normal. Escríbala sin espacios | Cuenta de Google, Seguridad, Contraseñas de aplicaciones | `abcdefghijklmnop` |
| `EMAIL_HOST` | No | Servidor SMTP con SSL. Por defecto `smtp.gmail.com` | Su proveedor de correo | `smtp.gmail.com` |
| `EMAIL_PORT` | No | Puerto SMTP SSL. Por defecto 465 | Su proveedor de correo | `465` |
| `TRELLO_API_KEY` | Solo para Trello | Clave de la API de Trello. No está en `.env.sample` | https://trello.com/power-ups/admin | `clave-trello-ejemplo` |
| `TRELLO_API_TOKEN` | Solo para Trello | Token de la API de Trello. No está en `.env.sample` | Se genera desde la clave anterior | `token-trello-ejemplo` |
| `TRELLO_DEFAULT_LIST_ID` | No | Lista donde se crean tarjetas cuando la petición no trae `trello_list_id`. No está en `.env.sample` | Identificador de la lista en Trello | `lista-ejemplo` |
| `MY_PROJECT` | No | Nombre mostrado en `GET /`. Por defecto `IntelliAgent`. Compose lo fija | n/a | `IntelliAgent` |
| `PORT` | No | Compose lo fija en `8000`. El código no lo lee | n/a | `8000` |
| `VITE_API_URL` | No | Base de la API en el frontend, solo en tiempo de compilación. Por defecto `/api` | n/a | `/api` |

Notas:

- `.env.sample-db` lista `POSTGRES_USER`, `POSTGRES_PASSWORD` y `POSTGRES_DB`, pero Compose no lo lee: esos tres valores están escritos dentro de `compose.yaml` y `compose.prod.yaml`.
- Sin `EMAIL_*` el backend arranca, pero el envío y la lectura de correo fallan al usarse. Sin `TRELLO_*` la creación de tarjetas falla al usarse.
- `compose.yaml` define `VITE_API_URL=http://localhost:8080/api` en el servicio `frontend`, pero no tiene efecto: el valor que cuenta es el argumento de compilación, que por defecto es `/api`, y Nginx reenvía `/api/` al backend.

## 8. Verificar el entorno con check_setup.py

El repositorio incluye un script que revisa `.env`, las variables, Docker, Docker Compose y la existencia de los archivos del proyecto. Se ejecuta con Python 3 desde la raíz:

```bash
python check_setup.py
```

Resultado esperado: una lista de comprobaciones y un código de salida 0 si todo está bien, 1 si algo falla.

Advertencias:

- Imprime los primeros 10 caracteres del valor de cada variable. No lo ejecute mientras comparte pantalla ni pegue su salida en un lugar público.
- Pide copiar `.env.example`, que ahora existe, y sugiere `docker-compose up --build` (con guion). Con Compose v2 el comando es `docker compose up --build`.
- En Windows, con la consola en cp1252, falla con `UnicodeEncodeError` al imprimir los emojis. Ejecútelo con UTF-8 activado: en Git Bash `PYTHONUTF8=1 python check_setup.py`; en PowerShell `$env:PYTHONUTF8 = "1"; python check_setup.py`.
- Reporta Docker como no encontrado si Docker no está en el PATH, aunque el resto de las comprobaciones pasen.

## 9. Verifica que funciona

Con los tres contenedores arriba:

- [ ] `docker compose ps` muestra `intelliagent_db` como `healthy` y los otros dos como `running`.
- [ ] `curl http://localhost:8080/` devuelve un JSON con el mensaje de bienvenida de la API.
- [ ] `curl http://localhost:8080/api/research/` responde `{"status":"ok","module":"research"}`. Es el endpoint de salud del módulo de investigación; no hay un `/healthz`.
- [ ] http://localhost:8080/docs abre la documentación interactiva de FastAPI.
- [ ] http://localhost:3000 muestra el formulario "Nueva Investigación" y la lista "Investigaciones Recientes".
- [ ] `curl http://localhost:3000/api/research/` responde igual que el puerto 8080 (prueba el proxy de Nginx).
- [ ] Crear una investigación desde el formulario la deja en estado `pending` o `processing` y después en `completed`. Si queda en `failed`, revise `docker compose logs backend`: lo más probable es una clave de OpenAI inválida.
- [ ] Opcional: `docker compose exec db_service psql -U <USUARIO> -d <BASE> -c "\dt"` lista las tablas `chatmessage`, `researchtask` y `researchresult`.

Ejemplos de peticiones con `curl`, Python y Node: [API_EXAMPLES.md](../API_EXAMPLES.md).

## 10. Solución de problemas

| Síntoma | Causa | Qué hacer |
|---|---|---|
| `Bind for 0.0.0.0:3000 failed: port is already allocated` (o 8080, o 5433) | Otro proceso usa ese puerto | Cierre el otro proceso o cambie el lado izquierdo del mapeo en `compose.yaml`, por ejemplo `3001:80`. El puerto 5433 existe justamente para no chocar con un PostgreSQL local en 5432 |
| El backend sale con `NotImplementedError: 'API_KEY' was not set` | Falta `API_KEY` en `.env` | Defínala. Con Compose, recree el contenedor: `docker compose up -d backend` |
| El backend sale con `NotImplementedError: OPENAI_API_KEY is required` | Falta `OPENAI_API_KEY` | Defínala en `.env` y recree el contenedor |
| `AttributeError: 'NoneType' object has no attribute 'replace'` al arrancar | `DATABASE_URL` no está definida. El código solo comprueba la cadena vacía, no la ausencia | Defínala en `.env`. Sin Docker, expórtela antes de lanzar `uvicorn` |
| `Can't load plugin: sqlalchemy.dialects:postgresql.psycopg2` o `No module named 'psycopg2'` | `DATABASE_URL` empieza por `postgresql://` | Use el prefijo `postgresql+psycopg://` |
| `Can't load plugin: sqlalchemy.dialects:postgres.psycopg` | `DATABASE_URL` empieza por `postgres://` y el código lo reescribe a un dialecto que SQLAlchemy 2 no tiene | Use el prefijo `postgresql+psycopg://` |
| `password authentication failed` o `database "..." does not exist` | Usuario, clave o base de `DATABASE_URL` no coinciden con los de `compose.yaml`. Si cambió esos valores después de la primera ejecución, el volumen conserva los antiguos | Ajuste `DATABASE_URL`. Si no importa perder datos: `docker compose down -v` y vuelva a levantar |
| `could not translate host name "db_service"` o conexión rechazada al correr sin Docker | `DATABASE_URL` apunta al host de la red de Compose | Use `localhost:5433` fuera de Docker |
| `curl: (52)` o `502 Bad Gateway` en http://localhost:3000/api/ | El backend aún no arrancó o falló | `docker compose logs backend`. Espere a `Application startup complete` |
| Con `npm run dev`, el frontend muestra errores de red o `ENOTFOUND backend` | El proxy de Vite apunta al host `backend` | Aplique la opción A o B de la sección 6.3 |
| Cambié código del frontend y no se refleja en http://localhost:3000 | El contenedor sirve archivos ya compilados | `docker compose up --build -d frontend` |
| Error de CORS en el navegador | CORS acepta cualquier origen (`allow_origins=["*"]`), así que rara vez es la causa. Suele ser una URL de API equivocada | Confirme que el frontend llama a `/api` y que el backend responde en http://localhost:8080 |
| La investigación queda `completed` pero el correo o la tarjeta de Trello no llegan | Los errores de correo y Trello solo se imprimen en la salida estándar y no cambian el estado | `docker compose logs backend`. Revise `EMAIL_*` (con contraseña de aplicación) y `TRELLO_*` |
| Las fuentes y los datos clave de los resultados parecen siempre iguales | `key_data` y `sources` se guardan con valores fijos, y la herramienta `web_search` está simulada | Es el comportamiento actual del código, no un fallo de la instalación |
| `pip install` falla por la versión de Python | Se usa una versión distinta de 3.13 | Instale Python 3.13 o use la ruta con Docker |
| `npm install` o `npm run dev` fallan por la versión de Node | Se usa una versión muy distinta de 20 | Instale Node 20 |
| Una tabla no tiene una columna nueva después de cambiar un modelo | No hay migraciones y `create_all` no altera tablas existentes | Para desarrollo: `docker compose down -v` y levantar de nuevo. Con datos que conservar, hay que alterar la tabla a mano con SQL |
