import json
from typing import List, Dict
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
import requests
import os

from api.integrations.trello import create_trello_card
from api.myemailer.sender import send_mail


@tool
def web_search(query: str) -> str:
    """
    Realiza una búsqueda web sobre un tema específico.

    Args:
        query: Término o pregunta a buscar en la web

    Returns:
        Resultados de búsqueda en formato texto
    """
    # Simulación de búsqueda web - en producción usar API real como Tavily, Serper, etc.
    # Por ahora retornamos un resultado simulado
    return f"""
    Resultados de búsqueda para: {query}

    Fuente 1: Wikipedia
    Información relevante sobre {query}. Este es un contenido de ejemplo que describe
    los aspectos principales del tema consultado. En una implementación real, esto vendría
    de una API de búsqueda web real.

    Fuente 2: Artículos académicos
    Estudios recientes muestran que {query} tiene múltiples aplicaciones y beneficios.
    Los expertos recomiendan investigar más a fondo para obtener mejores resultados.

    Fuente 3: Noticias recientes
    Las últimas noticias sobre {query} indican un creciente interés en el tema.
    """


@tool
def summarize_text(text: str, max_length: int = 500) -> str:
    """
    Genera un resumen conciso de un texto largo.

    Args:
        text: Texto a resumir
        max_length: Longitud máxima del resumen en palabras

    Returns:
        Resumen del texto
    """
    try:
        llm = ChatOpenAI(temperature=0)
        prompt = f"""
        Por favor, crea un resumen conciso y coherente del siguiente texto.
        El resumen no debe exceder {max_length} palabras.

        Texto:
        {text}

        Resumen:
        """
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error al generar resumen: {str(e)}"


@tool
def extract_key_data(text: str, config: RunnableConfig) -> str:
    """
    Extrae datos clave de un texto y los estructura en formato JSON.

    Args:
        text: Texto del cual extraer datos clave
        config: Configuración del agente

    Returns:
        Datos clave en formato JSON string
    """
    try:
        llm = ChatOpenAI(temperature=0)
        prompt = f"""
        Analiza el siguiente texto y extrae los datos clave más importantes.
        Devuelve SOLO un objeto JSON válido con esta estructura:
        {{
            "tema_principal": "descripción breve",
            "puntos_clave": ["punto 1", "punto 2", "punto 3"],
            "datos_importantes": {{"clave": "valor"}},
            "conclusiones": "resumen de conclusiones"
        }}

        Texto:
        {text}

        JSON:
        """
        response = llm.invoke(prompt)
        content = response.content.strip()

        # Limpiar el contenido si viene con markdown
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        # Validar que sea JSON válido
        json.loads(content)

        return content
    except Exception as e:
        # Retornar JSON de error válido
        return json.dumps({
            "error": str(e),
            "tema_principal": "Error al procesar",
            "puntos_clave": [],
            "datos_importantes": {},
            "conclusiones": "No se pudo extraer información"
        })


@tool
def create_task_card(title: str, description: str, list_id: str = None) -> str:
    """
    Crea una tarjeta de tarea en Trello.

    Args:
        title: Título de la tarjeta
        description: Descripción detallada de la tarea
        list_id: ID de la lista de Trello (opcional, usa variable de entorno si no se proporciona)

    Returns:
        Mensaje de confirmación o error
    """
    try:
        if not list_id:
            list_id = os.environ.get("TRELLO_DEFAULT_LIST_ID")
            if not list_id:
                return "Error: No se proporcionó list_id y TRELLO_DEFAULT_LIST_ID no está configurado"

        result = create_trello_card(list_id, title, description)

        if result.get("success"):
            return f"Tarjeta creada exitosamente. URL: {result.get('card_url')}"
        else:
            return f"Error al crear tarjeta: {result.get('error')}"
    except Exception as e:
        return f"Error al crear tarjeta en Trello: {str(e)}"


@tool
def send_research_email(subject: str, content: str, recipient: str = None) -> str:
    """
    Envía un correo electrónico con los resultados de la investigación.

    Args:
        subject: Asunto del correo
        content: Contenido del correo
        recipient: Dirección de correo del destinatario (opcional)

    Returns:
        Mensaje de confirmación o error
    """
    try:
        # Si no se proporciona destinatario, enviar al email configurado por defecto
        if not recipient:
            recipient = os.environ.get("EMAIL_ADDRESS")

        send_mail(subject=subject, content=content, to_email=recipient)
        return f"Correo enviado exitosamente a {recipient}"
    except Exception as e:
        return f"Error al enviar correo: {str(e)}"


@tool
def research_and_analyze(topic: str, config: RunnableConfig) -> Dict:
    """
    Herramienta completa que investiga un tema, genera resumen y extrae datos clave.

    Args:
        topic: Tema a investigar
        config: Configuración del agente

    Returns:
        Diccionario con resultados de investigación
    """
    try:
        # 1. Buscar información
        search_results = web_search.invoke(topic)

        # 2. Generar resumen
        summary = summarize_text.invoke(search_results)

        # 3. Extraer datos clave
        key_data_str = extract_key_data.invoke(search_results, config)

        result = {
            "topic": topic,
            "summary": summary,
            "key_data": key_data_str,
            "sources": ["Web Search", "AI Analysis"],
            "status": "completed"
        }

        return result
    except Exception as e:
        return {
            "topic": topic,
            "summary": "",
            "key_data": json.dumps({"error": str(e)}),
            "sources": [],
            "status": "failed"
        }


# Lista de herramientas para investigación
RESEARCH_TOOLS = [
    web_search,
    summarize_text,
    extract_key_data,
]

# Lista de herramientas para integración
INTEGRATION_TOOLS = [
    create_task_card,
    send_research_email,
]

# Todas las herramientas de investigación
ALL_RESEARCH_TOOLS = RESEARCH_TOOLS + INTEGRATION_TOOLS + [research_and_analyze]
