import datetime
import uuid
from typing import Any

from sqlalchemy import JSON, DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class CalculationResultRow(Base):
    """One stored calculation result (``calculation-api`` design.md decision 4).

    ``JSON`` is PostgreSQL ``json``, which keeps the text as written, so a stored
    envelope reads back equal to the one returned. A row is never updated.
    """

    __tablename__ = "calculation_result"

    result_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    calculation_type: Mapped[str] = mapped_column(String(200))
    engine_version: Mapped[str] = mapped_column(String(50))
    input_hash: Mapped[str] = mapped_column(String(64), index=True)
    inputs: Mapped[dict[str, Any]] = mapped_column(JSON)
    envelope: Mapped[dict[str, Any]] = mapped_column(JSON)
    norm_sources: Mapped[list[dict[str, str]]] = mapped_column(JSON)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
