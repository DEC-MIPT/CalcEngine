import datetime
import uuid
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class FoundationContextRow(Base):
    __tablename__ = "foundation_context"

    result_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("calculation_result.result_id"), primary_key=True)
    context: Mapped[dict[str, Any]] = mapped_column(JSON)


class FoundationSelectionRow(Base):
    __tablename__ = "foundation_selection"

    selection_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    input_hash: Mapped[str] = mapped_column(String(64), index=True)
    selected_result_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("calculation_result.result_id"), nullable=True)
    outcome: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
