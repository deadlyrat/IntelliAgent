# IntelliAgent - Ejemplos de API

Este archivo contiene ejemplos de cómo usar la API de IntelliAgent usando `curl` o herramientas similares.

## Base URL

```
http://localhost:8080
```

---

## Endpoints de Investigación

### 1. Crear Nueva Investigación

**Endpoint**: `POST /api/research/tasks/`

```bash
# Investigación simple
curl -X POST http://localhost:8080/api/research/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Inteligencia Artificial en la medicina",
    "send_email": false,
    "create_trello_card": false
  }'
```

```bash
# Con envío de email
curl -X POST http://localhost:8080/api/research/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Blockchain y criptomonedas",
    "send_email": true,
    "email_address": "tu-email@ejemplo.com",
    "create_trello_card": false
  }'
```

```bash
# Con creación de tarjeta en Trello
curl -X POST http://localhost:8080/api/research/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Energías renovables",
    "send_email": false,
    "create_trello_card": true,
    "trello_list_id": "tu-list-id-aqui"
  }'
```

```bash
# Completo: Con email y Trello
curl -X POST http://localhost:8080/api/research/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Machine Learning en finanzas",
    "send_email": true,
    "email_address": "tu-email@ejemplo.com",
    "create_trello_card": true,
    "trello_list_id": "tu-list-id-aqui"
  }'
```

**Respuesta Exitosa**:
```json
{
  "id": 1,
  "topic": "Inteligencia Artificial en la medicina",
  "status": "pending",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "result": null
}
```

---

### 2. Listar Todas las Investigaciones

**Endpoint**: `GET /api/research/tasks/`

```bash
curl http://localhost:8080/api/research/tasks/
```

**Respuesta**:
```json
[
  {
    "id": 1,
    "topic": "Inteligencia Artificial en la medicina",
    "status": "completed",
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:31:00Z",
    "result": {
      "id": 1,
      "task_id": 1,
      "summary": "La IA está revolucionando la medicina...",
      "key_data": {
        "tema_principal": "IA en medicina",
        "puntos_clave": ["Diagnóstico", "Tratamiento", "Investigación"],
        "datos_importantes": {},
        "conclusiones": "La IA tiene un gran potencial..."
      },
      "sources": ["Web Search", "AI Analysis"],
      "created_at": "2025-01-15T10:31:00Z"
    }
  }
]
```

---

### 3. Obtener Investigación Específica

**Endpoint**: `GET /api/research/tasks/{task_id}`

```bash
curl http://localhost:8080/api/research/tasks/1
```

---

### 4. Eliminar Investigación

**Endpoint**: `DELETE /api/research/tasks/{task_id}`

```bash
curl -X DELETE http://localhost:8080/api/research/tasks/1
```

**Respuesta**:
```json
{
  "message": "Tarea eliminada exitosamente"
}
```

---

## Endpoints de Chat (Sistema Original)

### 1. Enviar Mensaje al Agente

**Endpoint**: `POST /api/chats/`

```bash
# Investigación y email
curl -X POST http://localhost:8080/api/chats/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Research about renewable energy and email me the results"
  }'
```

```bash
# Consulta general
curl -X POST http://localhost:8080/api/chats/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about the benefits of solar energy"
  }'
```

---

### 2. Listar Mensajes Recientes

**Endpoint**: `GET /api/chats/recent/`

```bash
curl http://localhost:8080/api/chats/recent/
```

---

## Endpoint de Salud

### Verificar Estado del Backend

```bash
# Root endpoint
curl http://localhost:8080/

# Research health
curl http://localhost:8080/api/research/

# Chat health
curl http://localhost:8080/api/chats/
```

---

## Usando Python

### Con requests

```python
import requests
import json

# Crear investigación
url = "http://localhost:8080/api/research/tasks/"
data = {
    "topic": "Inteligencia Artificial",
    "send_email": False,
    "create_trello_card": False
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), indent=2))

# Listar investigaciones
response = requests.get(url)
tasks = response.json()
for task in tasks:
    print(f"{task['id']}: {task['topic']} - {task['status']}")
```

---

## Usando JavaScript (Node.js)

```javascript
// Crear investigación
const axios = require('axios');

async function createResearch() {
  const response = await axios.post('http://localhost:8080/api/research/tasks/', {
    topic: 'Inteligencia Artificial',
    send_email: false,
    create_trello_card: false
  });

  console.log(response.data);
}

// Listar investigaciones
async function listResearch() {
  const response = await axios.get('http://localhost:8080/api/research/tasks/');
  response.data.forEach(task => {
    console.log(`${task.id}: ${task.topic} - ${task.status}`);
  });
}

createResearch();
```

---

## Usando Postman

### Importar Colección

Puedes crear una colección en Postman con estos endpoints:

1. **Crear Investigación**
   - Method: POST
   - URL: `http://localhost:8080/api/research/tasks/`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
   ```json
   {
     "topic": "Tu tema aquí",
     "send_email": false,
     "create_trello_card": false
   }
   ```

2. **Listar Investigaciones**
   - Method: GET
   - URL: `http://localhost:8080/api/research/tasks/`

3. **Obtener Investigación**
   - Method: GET
   - URL: `http://localhost:8080/api/research/tasks/1`

4. **Eliminar Investigación**
   - Method: DELETE
   - URL: `http://localhost:8080/api/research/tasks/1`

---

## Estados de Investigación

- `pending`: Investigación creada, esperando procesamiento
- `processing`: Investigación en progreso
- `completed`: Investigación completada exitosamente
- `failed`: Investigación falló

---

## Notas Importantes

1. La investigación se procesa en segundo plano
2. Consulta el estado periódicamente para ver cuándo se completa
3. Los resultados incluyen resumen, datos clave y fuentes
4. El email y Trello son opcionales pero requieren configuración previa

---

## Documentación Interactiva

Para explorar la API de forma interactiva, visita:
```
http://localhost:8080/docs
```

Esta interfaz Swagger UI te permite probar todos los endpoints directamente desde el navegador.
