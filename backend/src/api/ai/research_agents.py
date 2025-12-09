from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from api.ai.llms import get_openai_llm
from api.ai.research_tools import (
    web_search,
    summarize_text,
    extract_key_data,
    create_task_card,
    send_research_email,
    RESEARCH_TOOLS,
    INTEGRATION_TOOLS,
)


def get_web_research_agent():
    """
    Agente especializado en búsqueda e investigación web
    """
    model = get_openai_llm()
    agent = create_react_agent(
        model=model,
        tools=[web_search],
        prompt="""Eres un asistente de investigación web experto. Tu trabajo es:
        1. Buscar información relevante sobre el tema solicitado
        2. Encontrar múltiples fuentes confiables
        3. Proporcionar resultados detallados y precisos

        Siempre cita tus fuentes y proporciona información verificable.""",
        name="web_research_agent"
    )
    return agent


def get_summary_agent():
    """
    Agente especializado en generación de resúmenes
    """
    model = get_openai_llm()
    agent = create_react_agent(
        model=model,
        tools=[summarize_text],
        prompt="""Eres un experto en síntesis de información. Tu trabajo es:
        1. Analizar textos largos y complejos
        2. Extraer las ideas principales
        3. Crear resúmenes concisos y coherentes
        4. Mantener la precisión de la información original

        Los resúmenes deben ser claros, informativos y fáciles de entender.""",
        name="summary_agent"
    )
    return agent


def get_data_extraction_agent():
    """
    Agente especializado en extracción de datos clave
    """
    model = get_openai_llm()
    agent = create_react_agent(
        model=model,
        tools=[extract_key_data],
        prompt="""Eres un analista de datos experto. Tu trabajo es:
        1. Identificar datos clave en textos
        2. Estructurar información en formato JSON
        3. Extraer puntos importantes y conclusiones
        4. Organizar la información de manera lógica

        Siempre devuelve datos estructurados y bien formateados.""",
        name="data_extraction_agent"
    )
    return agent


def get_integration_agent():
    """
    Agente especializado en integraciones con servicios externos
    """
    model = get_openai_llm()
    agent = create_react_agent(
        model=model,
        tools=INTEGRATION_TOOLS,
        prompt="""Eres un asistente de integración. Tu trabajo es:
        1. Crear tareas en Trello cuando se solicite
        2. Enviar correos electrónicos con resultados
        3. Gestionar comunicaciones con servicios externos

        Confirma cada acción realizada y reporta cualquier error.""",
        name="integration_agent"
    )
    return agent


def get_complete_research_agent():
    """
    Agente completo con todas las herramientas de investigación
    """
    model = get_openai_llm()
    agent = create_react_agent(
        model=model,
        tools=RESEARCH_TOOLS + INTEGRATION_TOOLS,
        prompt="""Eres IntelliAgent, un asistente de investigación inteligente y completo.

        Tus capacidades incluyen:
        - Investigación web exhaustiva
        - Generación de resúmenes concisos
        - Extracción de datos clave en formato JSON
        - Creación de tareas en Trello
        - Envío de correos electrónicos

        Proceso recomendado:
        1. Investiga el tema usando web_search
        2. Analiza y resume la información con summarize_text
        3. Extrae datos clave con extract_key_data
        4. Si se solicita, crea tareas en Trello o envía emails

        Siempre proporciona resultados completos, precisos y bien estructurados.""",
        name="complete_research_agent"
    )
    return agent


def get_research_supervisor(checkpointer=None):
    """
    Supervisor que coordina múltiples agentes especializados
    """
    llm = get_openai_llm()

    # Crear agentes especializados
    web_agent = get_web_research_agent()
    summary_agent = get_summary_agent()
    data_agent = get_data_extraction_agent()
    integration_agent = get_integration_agent()

    # Crear supervisor
    supervisor = create_supervisor(
        agents=[web_agent, summary_agent, data_agent, integration_agent],
        model=llm,
        prompt="""Eres el supervisor de IntelliAgent, un sistema de investigación inteligente.

        Gestiona estos agentes especializados:
        - web_research_agent: Búsqueda de información en la web
        - summary_agent: Generación de resúmenes
        - data_extraction_agent: Extracción de datos a JSON
        - integration_agent: Integraciones con Trello y email

        Delega tareas de manera eficiente:
        1. Asigna investigación web al web_research_agent
        2. Pasa los resultados al summary_agent para resumir
        3. Usa data_extraction_agent para estructurar datos
        4. Usa integration_agent para enviar emails o crear tareas

        Coordina el flujo de trabajo para obtener los mejores resultados.""",
    ).compile(checkpointer=checkpointer)

    return supervisor
