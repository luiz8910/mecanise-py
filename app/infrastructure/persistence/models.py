from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class PartRequestRecord(SQLModel, table=True):
    """
    Registro persistido do pedido (payload JSON + metadados).
    """
    id: str = Field(default_factory=lambda: f"req_{datetime.utcnow().timestamp():.0f}", primary_key=True)
    status: str = Field(default="COLLECTING_QUOTES", index=True)
    payload: str
    source: Optional[str] = Field(default=None, index=True)  # ex.: phone do WhatsApp
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)
