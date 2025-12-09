from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, DateTime, Column, TEXT, JSON
import json


def get_utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)


class ResearchTaskPayload(SQLModel):
    """Modelo para recibir solicitudes de investigación"""
    topic: str
    send_email: bool = False
    email_address: Optional[str] = None
    create_trello_card: bool = False
    trello_list_id: Optional[str] = None


class ResearchTask(SQLModel, table=True):
    """Tabla para almacenar tareas de investigación"""
    id: int | None = Field(default=None, primary_key=True)
    topic: str = Field(index=True)
    status: str = Field(default="pending")  # pending, processing, completed, failed
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False,
    )


class ResearchResult(SQLModel, table=True):
    """Tabla para almacenar resultados de investigación"""
    id: int | None = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="researchtask.id", index=True)
    summary: str = Field(sa_column=Column(TEXT))
    key_data: str = Field(sa_column=Column(TEXT))  # JSON string
    sources: str = Field(sa_column=Column(TEXT))  # JSON array of sources
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False,
    )

    def get_key_data_dict(self):
        """Convierte el JSON string a diccionario"""
        try:
            return json.loads(self.key_data)
        except:
            return {}

    def get_sources_list(self):
        """Convierte el JSON string de fuentes a lista"""
        try:
            return json.loads(self.sources)
        except:
            return []


class ResearchResultResponse(SQLModel):
    """Modelo para respuestas de resultados de investigación"""
    id: int
    task_id: int
    summary: str
    key_data: dict
    sources: list
    created_at: datetime


class ResearchTaskResponse(SQLModel):
    """Modelo para respuestas de tareas de investigación"""
    id: int
    topic: str
    status: str
    created_at: datetime
    updated_at: datetime
    result: Optional[ResearchResultResponse] = None
