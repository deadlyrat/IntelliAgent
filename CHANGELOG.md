# Changelog

Todos los cambios relevantes de IntelliAgent se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).
El repositorio no tiene etiquetas ni versiones publicadas, por eso las entradas se agrupan por fecha de commit.

## [Sin versionar]

### Agregado

- Documentación completa en `docs/`: guía de instalación, despliegue, arquitectura, base de datos y API.
- `.env.example` con todas las variables que lee el código, incluidas las de Trello y correo que faltan en `.env.sample`.
- `SECURITY.md` con la política de reporte y las limitaciones de seguridad conocidas.
- Este `CHANGELOG.md`.

## 2026-10-04

### Agregado

- Banner y recursos visuales para el README (2db115c).
- Licencia MIT (2a53802).

### Cambiado

- README reescrito (d5a60e2).
- Merge del pull request #1, `docs/portafolio-v3` (0f3caaf).

## 2026-05-21

### Agregado

- README de portafolio (40888fa).

### Cambiado

- README de portafolio v2 en español, con iconos y diagrama Mermaid (c074f66, 35c8048, 0ddc5b6).

## 2025-12-09

### Agregado

- Agentes de investigación, integración con Trello y frontend (5aff442).

## 2025-06-14

### Cambiado

- Actualización de `README.md` (58ef244).

## 2025-06-13

### Agregado

- Plantilla de variables de entorno `.env.sample` (699008e).
- `thread_id` y checkpointer en los agentes (e574923).
- Supervisor LangGraph como endpoint de FastAPI, configuración ejecutable con herramientas de LangChain, conexión de varios agentes con LangGraph Supervisor y agente de investigación con LangGraph.
- Llamada a herramientas con LangChain y LangGraph, y herramientas para agentes con LangChain.

## 2025-06-12

### Agregado

- Envío de correo con Python y FastAPI, y lectura de la bandeja de entrada de Gmail con Python.
- LangChain con FastAPI y SQLModel, salida estructurada con LangChain y LangChain con Docker Model Runner.
- Modelos de base de datos, ruta para crear mensajes de chat, rutas anidadas en FastAPI y comandos curl para crear y listar datos.
- Compose con Postgres y volúmenes administrados por Docker, e integración de Postgres con FastAPI y SQLModel.
- Despliegue con campo de marca de tiempo y comentarios para producción.

## 2025-06-11

### Agregado

- Configuración de Railway y patrones de vigilancia actualizados.
- Archivo de exclusión de Docker, volúmenes, modo watch de Compose e inyección de contraseñas y secretos en tiempo de ejecución.
- Servicio "Hello World" con Docker y FastAPI.

### Seguridad

- Retirada de una clave de API que había quedado expuesta en el código (commits "Removed exposed api key", "Check api key encryption" y "Removed api key exposure").

## 2025-06-10

### Agregado

- Primer servicio con Docker Compose, imagen personalizada, Dockerfile para servir HTML y copia de archivos locales al contenedor.
- `.gitignore` de Python y README inicial.
- Acceso a servidores web de Python dentro de Docker.
