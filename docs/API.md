# API

Referencia de las rutas HTTP que expone el backend FastAPI (`backend/src/main.py` y los routers de `backend/src/api/`). Las respuestas son JSON. Los nombres de campos y rutas se mantienen tal como están en el código.

Para el flujo interno de una investigación ver [ARQUITECTURA.md](ARQUITECTURA.md). Para las tablas que usa cada ruta ver [BASE_DE_DATOS.md](BASE_DE_DATOS.md). Ejemplos adicionales en [API_EXAMPLES.md](../API_EXAMPLES.md).

## Convenciones

### URL base

| Entorno | URL |
|---|---|
| Compose (desarrollo o producción) | `http://localhost:8080` (puerto del backend). A través de Nginx también está disponible en `http://localhost:3000/api/` |
| Documentación interactiva (Swagger UI) | `http://localhost:8080/docs` |

En los ejemplos se usa `<BASE_URL>` como marcador. Sustitúyalo por la URL de su despliegue.

### Autenticación

Ninguna ruta exige autenticación ni autorización. La variable `API_KEY` solo se comprueba que exista al arrancar el backend y no se usa para validar peticiones. Cualquier cliente con acceso de red puede crear, listar y borrar tareas y disparar envíos de correo y tarjetas de Trello. Los ejemplos de este documento no envían credenciales.

CORS permite cualquier origen (`allow_origins=["*"]`).

### Errores comunes

| Código | Cuerpo | Cuándo |
|---|---|---|
| 400 | `{ "detail": "Error with supervisor" }` | `POST /api/chats/` cuando el supervisor no devuelve resultado o mensajes |
| 404 | `{ "detail": "Tarea no encontrada" }` | `GET` o `DELETE` de una tarea que no existe |
| 422 | Detalle de validación de FastAPI | Cuerpo que no cumple el esquema (por ejemplo, falta `topic` o `message`) |
| 500 | Error interno | Fallo no controlado, por ejemplo base de datos inaccesible o error del proveedor del modelo en las rutas de chat |

### Resumen de rutas

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Mensaje de bienvenida |
| GET | `/api/chats/` | Salud del módulo de chat |
| GET | `/api/chats/recent/` | Hasta 10 mensajes de chat guardados |
| POST | `/api/chats/` | Envía un mensaje al supervisor y devuelve su respuesta |
| GET | `/api/research/` | Salud del módulo de investigación |
| GET | `/api/research/tasks/` | Las 20 tareas más recientes con su resultado |
| GET | `/api/research/tasks/{task_id}` | Una tarea y su resultado |
| POST | `/api/research/tasks/` | Crea una tarea y la procesa en segundo plano |
| DELETE | `/api/research/tasks/{task_id}` | Borra una tarea y sus resultados |

## Raíz

### GET /

Sin parámetros.

Respuesta 200:

```json
{
  "message": "Welcome to IntelliAgent API",
  "project": "IntelliAgent",
  "version": "1.0.0",
  "docs": "/docs"
}
```

`project` toma el valor de `MY_PROJECT` y, si no está definida, `IntelliAgent`.

```bash
curl <BASE_URL>/
```

## Investigación

Prefijo: `/api/research`. Es el módulo que usa el frontend.

### GET /api/research/

Salud del módulo. Respuesta 200:

```json
{ "status": "ok", "module": "research" }
```

```bash
curl <BASE_URL>/api/research/
```

### POST /api/research/tasks/

Crea una tarea con estado `pending`, devuelve de inmediato y procesa la investigación en segundo plano (`BackgroundTasks`).

Cuerpo (`ResearchTaskPayload`):

| Campo | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `topic` | cadena | Sí | n/a | Tema a investigar |
| `send_email` | booleano | No | `false` | Envía el resultado por correo |
| `email_address` | cadena o `null` | No | `null` | Destinatario. Si `send_email` es `true` y falta, el envío se omite sin error |
| `create_trello_card` | booleano | No | `false` | Crea una tarjeta en Trello con el resultado |
| `trello_list_id` | cadena o `null` | No | `null` | ID de la lista de Trello. Si `create_trello_card` es `true` y falta, la tarjeta se omite sin error |

Respuesta 200 (`ResearchTaskResponse`):

```json
{
  "id": 1,
  "topic": "Energías renovables",
  "status": "pending",
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T10:30:00Z",
  "result": null
}
```

Solo el tema:

```bash
curl -X POST <BASE_URL>/api/research/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "Energías renovables"}'
```

Con correo y tarjeta de Trello:

```bash
curl -X POST <BASE_URL>/api/research/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Energías renovables",
    "send_email": true,
    "email_address": "<CORREO_DESTINO>",
    "create_trello_card": true,
    "trello_list_id": "<ID_LISTA_TRELLO>"
  }'
```

El correo requiere `EMAIL_ADDRESS` y `EMAIL_PASSWORD`, y la tarjeta requiere `TRELLO_API_KEY` y `TRELLO_API_TOKEN`. Si la entrega falla, el error solo se imprime en el registro del backend y la tarea termina en `completed`.

### GET /api/research/tasks/

Lista las 20 tareas más recientes (`created_at` descendente). Cada una incluye su resultado si ya existe. Sin parámetros.

Respuesta 200: lista de `ResearchTaskResponse`.

```json
[
  {
    "id": 1,
    "topic": "Energías renovables",
    "status": "completed",
    "created_at": "2026-01-15T10:30:00Z",
    "updated_at": "2026-01-15T10:30:00Z",
    "result": {
      "id": 1,
      "task_id": 1,
      "summary": "<texto generado por el agente>",
      "key_data": { "info": "Datos extraídos por el agente" },
      "sources": ["Web Search", "AI Analysis"],
      "created_at": "2026-01-15T10:31:00Z"
    }
  }
]
```

`updated_at` conserva el valor de la creación porque el backend no lo actualiza al cambiar el estado. `key_data` y `sources` son valores fijos del código (ver [ARQUITECTURA.md](ARQUITECTURA.md#limitaciones-conocidas)).

```bash
curl <BASE_URL>/api/research/tasks/
```

### GET /api/research/tasks/{task_id}

Parámetro de ruta: `task_id` (entero). Respuesta 200: un `ResearchTaskResponse` con la misma forma que los elementos del listado. Respuesta 404 si no existe.

```bash
curl <BASE_URL>/api/research/tasks/1
```

### DELETE /api/research/tasks/{task_id}

Parámetro de ruta: `task_id` (entero). Elimina primero los resultados asociados y luego la tarea.

Respuesta 200:

```json
{ "message": "Tarea eliminada exitosamente" }
```

Respuesta 404 si no existe.

```bash
curl -X DELETE <BASE_URL>/api/research/tasks/1
```

### Esquemas

`ResearchTaskResponse`:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | entero | Identificador de la tarea |
| `topic` | cadena | Tema |
| `status` | cadena | `pending`, `processing`, `completed` o `failed` |
| `created_at` | fecha y hora ISO 8601 | Creación |
| `updated_at` | fecha y hora ISO 8601 | Ver la nota anterior |
| `result` | `ResearchResultResponse` o `null` | `null` mientras no hay resultado o si la tarea falló |

`ResearchResultResponse`:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | entero | Identificador del resultado |
| `task_id` | entero | Tarea asociada |
| `summary` | cadena | Contenido del último mensaje del agente |
| `key_data` | objeto | JSON guardado como texto y devuelto como objeto |
| `sources` | lista | JSON guardado como texto y devuelto como lista |
| `created_at` | fecha y hora ISO 8601 | Creación del resultado |

## Chat

Prefijo: `/api/chats`. El frontend no usa estas rutas.

### GET /api/chats/

Salud del módulo. Respuesta 200:

```json
{ "status": "ok" }
```

```bash
curl <BASE_URL>/api/chats/
```

### GET /api/chats/recent/

Devuelve hasta 10 mensajes guardados, sin orden explícito (el orden lo decide la base). Sin parámetros.

Respuesta 200 (lista de `ChatMessageListItem`):

```json
[
  {
    "id": 1,
    "message": "Investiga las ventajas de la energía solar",
    "created_at": "2026-01-15T10:30:00Z"
  }
]
```

```bash
curl <BASE_URL>/api/chats/recent/
```

### POST /api/chats/

Guarda el mensaje en la tabla `chatmessage`, invoca al supervisor (`email_agent` y `research_agent`) con una llamada síncrona y devuelve el contenido del último mensaje. La petición espera hasta que el modelo responde.

Cuerpo (`ChatMessagePayload`):

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `message` | cadena | Sí | Texto para el supervisor |

Respuesta 200 (`SupervisorMessageSchema`):

```json
{ "content": "<respuesta del supervisor>" }
```

Respuesta 400 con `{ "detail": "Error with supervisor" }` si el supervisor no devuelve resultado.

```bash
curl -X POST <BASE_URL>/api/chats/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Resume por qué conviene salir a caminar"}'
```

La herramienta `research_email` que usa este flujo tiene una inconsistencia conocida entre `response.content` y el campo `contents` del esquema (ver [ARQUITECTURA.md](ARQUITECTURA.md#limitaciones-conocidas)), por lo que las peticiones que preparen un correo pueden fallar con un error 500.

## Diferencias con API_EXAMPLES.md

[API_EXAMPLES.md](../API_EXAMPLES.md) coincide con las rutas, métodos y cuerpos del código. Las diferencias son de detalle:

| Tema | API_EXAMPLES.md | Código |
|---|---|---|
| `key_data` en las respuestas de ejemplo | Muestra `tema_principal`, `puntos_clave`, `datos_importantes` y `conclusiones` | El backend guarda siempre `{"info": "Datos extraídos por el agente"}`. La estructura de cuatro campos es la que devuelve la herramienta `extract_key_data`, pero no llega a la tabla |
| `sources` | Lo presenta como parte del resultado sin aclaración | Siempre `["Web Search", "AI Analysis"]` |
| Resumen de los resultados | "incluyen resumen, datos clave y fuentes" | La búsqueda web es simulada, así que el resumen no se apoya en fuentes reales |
| Fechas de ejemplo | Años 2025 | Solo ilustrativas, el backend usa la hora UTC actual |
| `updated_at` | Muestra un valor posterior en tareas completadas | No se actualiza: queda igual a `created_at` |
| Autenticación | No menciona que no existe | Ninguna ruta la exige |
| Puerto base | `http://localhost:8080` | Coincide con `compose.yaml` y `compose.prod.yaml` |
