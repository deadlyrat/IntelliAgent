# IntelliAgent

**Ecosistema Inteligente para la Automatización de la Investigación, Análisis y Gestión de Tareas**

---

## Descripción del Proyecto

IntelliAgent es un sistema de agentes de inteligencia artificial multifuncional desarrollado como proyecto final de la asignatura de Lenguajes de Programación. El sistema es capaz de realizar tareas complejas como investigación automatizada, síntesis de información, extracción de datos estructurados, y gestión de tareas en plataformas externas.

### Autores
- Pablo Aguirre
- José Herrera

### Institución
Universidad Tecnológica de Panamá
Facultad de Ingeniería de Sistemas Computacionales
Grupo: 1M3212

---

## Características Principales

- **Investigación Web Automatizada**: Búsqueda y recopilación de información sobre cualquier tema
- **Generación de Resúmenes**: Síntesis inteligente de textos largos en resúmenes concisos
- **Extracción de Datos**: Identificación y estructuración de datos clave en formato JSON
- **Integración con Trello**: Creación automática de tarjetas de tareas
- **Notificaciones por Email**: Envío automático de resultados de investigación
- **Interfaz Web Intuitiva**: Dashboard moderno para gestionar investigaciones
- **Arquitectura de Microservicios**: Completamente containerizada con Docker

---

## Tecnologías Utilizadas

### Backend
- **Python 3.12+**
- **FastAPI**: Framework web moderno y rápido
- **LangGraph**: Orquestación de agentes de IA
- **LangChain**: Framework para aplicaciones con LLM
- **OpenAI GPT**: Modelo de lenguaje para investigación y análisis
- **SQLModel**: ORM para gestión de base de datos
- **PostgreSQL**: Base de datos relacional
- **Uvicorn**: Servidor ASGI de alto rendimiento

### Frontend
- **React 18**: Librería de UI
- **Vite**: Build tool y dev server
- **Axios**: Cliente HTTP
- **CSS3**: Estilos modernos

### DevOps
- **Docker**: Containerización
- **Docker Compose**: Orquestación de contenedores
- **Nginx**: Servidor web para el frontend

---

## Arquitectura del Sistema

```
┌─────────────────┐
│   Usuario       │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Frontend │ (React + Nginx)
    │ Port 3000│
    └────┬─────┘
         │
    ┌────▼─────────┐
    │   Backend    │ (FastAPI)
    │   Port 8080  │
    └──┬────────┬──┘
       │        │
  ┌────▼───┐  ┌▼──────────────┐
  │PostgreSQL  │  Agentes IA   │
  │Port 5432│  │  (LangGraph)  │
  └─────────┘  └───┬───────────┘
                   │
         ┌─────────┴──────────┐
         │                    │
    ┌────▼────┐         ┌─────▼──────┐
    │ OpenAI  │         │   APIs     │
    │   API   │         │ Externas   │
    └─────────┘         │(Trello,etc)│
                        └────────────┘
```

---

## Instalación y Configuración

### Prerrequisitos

- Docker Desktop instalado
- Docker Compose
- Cuenta de OpenAI con API Key
- (Opcional) Cuenta de Trello con API credentials
- (Opcional) Cuenta de Gmail con contraseña de aplicación

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/intelliagent.git
cd intelliagent
```

### Paso 2: Configurar Variables de Entorno

1. Copiar el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Editar el archivo `.env` con tus credenciales:

```env
# API Configuration
API_KEY=tu-api-key-segura

# OpenAI (OBLIGATORIO)
OPENAI_API_KEY=sk-tu-api-key-de-openai
OPENAI_MODEL_NAME=gpt-4o-mini

# Email (Opcional)
EMAIL_ADDRESS=tu-email@gmail.com
EMAIL_PASSWORD=tu-contraseña-de-aplicacion

# Trello (Opcional)
TRELLO_API_KEY=tu-trello-api-key
TRELLO_API_TOKEN=tu-trello-token
TRELLO_DEFAULT_LIST_ID=id-de-tu-lista
```

### Paso 3: Construir y Ejecutar

```bash
# Construir e iniciar todos los servicios
docker-compose up --build

# O en segundo plano
docker-compose up -d --build
```

### Paso 4: Acceder a la Aplicación

- **Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8080
- **Documentación API**: http://localhost:8080/docs
- **PostgreSQL**: localhost:5432

---

## Uso de la Aplicación

### Crear una Nueva Investigación

1. Abre el navegador en http://localhost:3000
2. Ingresa el tema que deseas investigar
3. (Opcional) Marca las casillas para:
   - Enviar resultados por correo
   - Crear tarjeta en Trello
4. Haz clic en "Iniciar Investigación"
5. Los resultados aparecerán automáticamente cuando estén listos

### API Endpoints

#### Investigación

```bash
# Crear nueva investigación
POST /api/research/tasks/
{
  "topic": "Inteligencia Artificial en la medicina",
  "send_email": true,
  "email_address": "usuario@ejemplo.com",
  "create_trello_card": false
}

# Listar investigaciones
GET /api/research/tasks/

# Obtener investigación específica
GET /api/research/tasks/{task_id}

# Eliminar investigación
DELETE /api/research/tasks/{task_id}
```

#### Chat (Sistema original)

```bash
# Enviar mensaje al agente
POST /api/chats/
{
  "message": "Research about renewable energy and email me the results"
}

# Listar mensajes recientes
GET /api/chats/recent/
```

---

## Estructura del Proyecto

```
intelliagent/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── ai/
│   │   │   │   ├── agents.py           # Agentes de email
│   │   │   │   ├── research_agents.py  # Agentes de investigación
│   │   │   │   ├── research_tools.py   # Herramientas de IA
│   │   │   │   ├── llms.py            # Configuración LLM
│   │   │   │   └── ...
│   │   │   ├── chat/
│   │   │   │   ├── models.py          # Modelos de chat
│   │   │   │   └── routing.py         # Endpoints de chat
│   │   │   ├── research/
│   │   │   │   ├── models.py          # Modelos de investigación
│   │   │   │   └── routing.py         # Endpoints de investigación
│   │   │   ├── integrations/
│   │   │   │   └── trello.py          # Cliente de Trello
│   │   │   ├── myemailer/
│   │   │   │   └── sender.py          # Envío de emails
│   │   │   └── db.py                  # Configuración BD
│   │   └── main.py                    # Punto de entrada
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Componente principal
│   │   ├── main.jsx                   # Punto de entrada
│   │   └── index.css                  # Estilos
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
├── compose.yaml                       # Docker Compose
├── .env.example                       # Variables de ejemplo
└── README.md                          # Este archivo
```

---

## Casos de Uso

### CU-01: Realizar Investigación y Recibir Resumen

**Actor**: Usuario final
**Flujo**:
1. Usuario ingresa tema en la UI
2. Backend recibe la petición
3. Agente de IA busca información y la resume
4. Sistema guarda resultados en BD
5. Sistema muestra resumen al usuario

### CU-02: Creación de Tarea en Trello

**Actor**: Usuario final
**Flujo**:
1. Usuario selecciona opción de Trello
2. Proporciona ID de lista
3. Backend envía datos a API de Trello
4. Se crea tarjeta con información relevante
5. Sistema confirma creación

### CU-03: Envío de Resultados por Correo

**Actor**: Usuario final
**Flujo**:
1. Usuario selecciona opción de email
2. Proporciona dirección de correo
3. Backend genera y envía correo
4. Usuario recibe resultados por email

---

## Comandos Útiles de Docker

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir un servicio específico
docker-compose up -d --build backend

# Ejecutar comando en contenedor
docker-compose exec backend bash

# Ver estado de los servicios
docker-compose ps
```

---

## Desarrollo

### Ejecutar Backend en Desarrollo

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

### Ejecutar Frontend en Desarrollo

```bash
cd frontend
npm install
npm run dev
```

---

## Troubleshooting

### Error: "OPENAI_API_KEY is required"

Asegúrate de haber configurado la variable `OPENAI_API_KEY` en tu archivo `.env`

### Error de conexión a base de datos

Verifica que el servicio de PostgreSQL esté corriendo:
```bash
docker-compose ps db_service
```

### Frontend no carga

1. Verifica que el backend esté corriendo en el puerto 8080
2. Revisa la configuración de CORS en `main.py`
3. Verifica la configuración de nginx en `frontend/nginx.conf`

### Emails no se envían

1. Verifica que uses una **contraseña de aplicación**, no tu contraseña regular de Gmail
2. Genera una en: https://myaccount.google.com/apppasswords
3. Asegúrate de tener la verificación en 2 pasos activada

---

## Requerimientos Funcionales Implementados

- ✅ RF-001: Iniciar tarea de investigación automatizada
- ✅ RF-002: Generar resumen a partir de múltiples fuentes
- ✅ RF-003: Extraer datos clave en formato JSON
- ✅ RF-004: Crear tareas automáticamente en Trello
- ✅ RF-005: Enviar resultados por correo electrónico
- ✅ RF-006: Almacenar resultados del proyecto
- ✅ RF-007: Visualizar resultados en interfaz de usuario

---

## Mejoras Futuras

- [ ] Implementar autenticación de usuarios
- [ ] Agregar búsqueda web real (Tavily, Serper API)
- [ ] Soporte para múltiples idiomas
- [ ] Exportación de resultados a PDF
- [ ] Integración con más servicios (Notion, Slack, etc.)
- [ ] Dashboard de analíticas
- [ ] Sistema de notificaciones en tiempo real
- [ ] Modo oscuro en la interfaz

---

## Licencia

Este proyecto es parte de un trabajo académico para la Universidad Tecnológica de Panamá.

---

## Contacto

Para preguntas o sugerencias, contactar a:
- Pablo Aguirre
- José Herrera

---

## Agradecimientos

- Prof. José Chiru - Facilitador de Lenguajes de Programación
- Universidad Tecnológica de Panamá
- Comunidad de LangChain y OpenAI

---

**Desarrollado con ❤️ para el curso de Lenguajes de Programación**
