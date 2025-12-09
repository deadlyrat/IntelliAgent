import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db import init_db
from api.chat.routing import router as chat_router
from api.research.routing import router as research_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup
    init_db()
    yield
    # after app startup

app = FastAPI(
    title="IntelliAgent API",
    description="Ecosistema Inteligente para la Automatización de la Investigación, Análisis y Gestión de Tareas",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(chat_router, prefix="/api/chats", tags=["Chat"])
app.include_router(research_router, prefix="/api/research", tags=["Research"])

MY_PROJECT = os.environ.get("MY_PROJECT") or "IntelliAgent"
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise NotImplementedError("'API_KEY' was not set")

@app.get("/", tags=["Root"])
def read_index():
    return {
        "message": "Welcome to IntelliAgent API",
        "project": MY_PROJECT,
        "version": "1.0.0",
        "docs": "/docs"
    }


# @app.get("/healthz")
# def heath_check():
#     return {"status": "ok"}