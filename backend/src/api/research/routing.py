import uuid
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from langgraph.checkpoint.memory import InMemorySaver

from api.db import get_session
from api.ai.research_agents import get_complete_research_agent, get_research_supervisor
from api.integrations.trello import create_trello_card
from api.myemailer.sender import send_mail
from .models import (
    ResearchTaskPayload,
    ResearchTask,
    ResearchResult,
    ResearchTaskResponse,
    ResearchResultResponse,
)

router = APIRouter()
checkpointer = InMemorySaver()


def process_research_task(
    task_id: int,
    topic: str,
    send_email: bool,
    email_address: str,
    create_trello: bool,
    trello_list_id: str,
    session: Session
):
    """
    Procesa una tarea de investigación en segundo plano
    """
    try:
        # Actualizar estado a processing
        task = session.get(ResearchTask, task_id)
        if not task:
            return

        task.status = "processing"
        session.add(task)
        session.commit()

        # Ejecutar investigación con el agente
        agent = get_complete_research_agent()
        thread_id = uuid.uuid4()

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"""Realiza una investigación completa sobre: {topic}

                        Por favor:
                        1. Busca información detallada sobre el tema
                        2. Genera un resumen conciso
                        3. Extrae los datos clave en formato JSON

                        Proporciona resultados completos y estructurados."""
                    }
                ]
            }
        )

        # Extraer información del resultado
        messages = result.get("messages", [])
        final_message = messages[-1] if messages else None

        if not final_message:
            raise Exception("No se obtuvo respuesta del agente")

        # Obtener el contenido
        summary = final_message.content

        # Intentar extraer JSON de datos clave
        # (esto dependerá de cómo el agente devuelva la información)
        key_data = {"info": "Datos extraídos por el agente"}
        sources = ["Web Search", "AI Analysis"]

        # Guardar resultado
        research_result = ResearchResult(
            task_id=task_id,
            summary=summary,
            key_data=json.dumps(key_data),
            sources=json.dumps(sources)
        )
        session.add(research_result)

        # Enviar email si se solicita
        if send_email and email_address:
            try:
                email_content = f"""
Investigación completada: {topic}

RESUMEN:
{summary}

DATOS CLAVE:
{json.dumps(key_data, indent=2, ensure_ascii=False)}

---
Generado por IntelliAgent
                """
                send_mail(
                    subject=f"Investigación: {topic}",
                    content=email_content,
                    to_email=email_address
                )
            except Exception as e:
                print(f"Error enviando email: {e}")

        # Crear tarjeta en Trello si se solicita
        if create_trello and trello_list_id:
            try:
                card_description = f"""
{summary}

Datos clave:
{json.dumps(key_data, indent=2, ensure_ascii=False)}
                """
                create_trello_card(
                    list_id=trello_list_id,
                    title=f"Investigación: {topic}",
                    description=card_description
                )
            except Exception as e:
                print(f"Error creando tarjeta en Trello: {e}")

        # Actualizar tarea a completada
        task.status = "completed"
        session.add(task)
        session.commit()

    except Exception as e:
        print(f"Error procesando investigación: {e}")
        # Actualizar tarea a fallida
        task = session.get(ResearchTask, task_id)
        if task:
            task.status = "failed"
            session.add(task)
            session.commit()


@router.get("/")
def research_health():
    """Endpoint de salud para el módulo de investigación"""
    return {"status": "ok", "module": "research"}


@router.get("/tasks/", response_model=List[ResearchTaskResponse])
def list_research_tasks(session: Session = Depends(get_session)):
    """Lista todas las tareas de investigación"""
    query = select(ResearchTask).order_by(ResearchTask.created_at.desc())
    tasks = session.exec(query).fetchall()[:20]

    response = []
    for task in tasks:
        # Buscar resultado si existe
        result_query = select(ResearchResult).where(ResearchResult.task_id == task.id)
        result = session.exec(result_query).first()

        task_response = ResearchTaskResponse(
            id=task.id,
            topic=task.topic,
            status=task.status,
            created_at=task.created_at,
            updated_at=task.updated_at,
            result=None
        )

        if result:
            task_response.result = ResearchResultResponse(
                id=result.id,
                task_id=result.task_id,
                summary=result.summary,
                key_data=result.get_key_data_dict(),
                sources=result.get_sources_list(),
                created_at=result.created_at
            )

        response.append(task_response)

    return response


@router.get("/tasks/{task_id}", response_model=ResearchTaskResponse)
def get_research_task(task_id: int, session: Session = Depends(get_session)):
    """Obtiene una tarea de investigación específica"""
    task = session.get(ResearchTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Buscar resultado
    result_query = select(ResearchResult).where(ResearchResult.task_id == task_id)
    result = session.exec(result_query).first()

    task_response = ResearchTaskResponse(
        id=task.id,
        topic=task.topic,
        status=task.status,
        created_at=task.created_at,
        updated_at=task.updated_at,
        result=None
    )

    if result:
        task_response.result = ResearchResultResponse(
            id=result.id,
            task_id=result.task_id,
            summary=result.summary,
            key_data=result.get_key_data_dict(),
            sources=result.get_sources_list(),
            created_at=result.created_at
        )

    return task_response


@router.post("/tasks/", response_model=ResearchTaskResponse)
def create_research_task(
    payload: ResearchTaskPayload,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    """
    Crea una nueva tarea de investigación

    El proceso se ejecuta en segundo plano y puede:
    - Investigar el tema proporcionado
    - Generar resumen
    - Extraer datos clave
    - Enviar email (opcional)
    - Crear tarjeta en Trello (opcional)
    """
    # Crear tarea
    task = ResearchTask(
        topic=payload.topic,
        status="pending"
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    # Iniciar procesamiento en segundo plano
    background_tasks.add_task(
        process_research_task,
        task_id=task.id,
        topic=payload.topic,
        send_email=payload.send_email,
        email_address=payload.email_address,
        create_trello=payload.create_trello_card,
        trello_list_id=payload.trello_list_id,
        session=session
    )

    return ResearchTaskResponse(
        id=task.id,
        topic=task.topic,
        status=task.status,
        created_at=task.created_at,
        updated_at=task.updated_at,
        result=None
    )


@router.delete("/tasks/{task_id}")
def delete_research_task(task_id: int, session: Session = Depends(get_session)):
    """Elimina una tarea de investigación"""
    task = session.get(ResearchTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Eliminar resultados asociados
    result_query = select(ResearchResult).where(ResearchResult.task_id == task_id)
    results = session.exec(result_query).all()
    for result in results:
        session.delete(result)

    session.delete(task)
    session.commit()

    return {"message": "Tarea eliminada exitosamente"}
