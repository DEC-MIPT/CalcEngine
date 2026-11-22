from uuid import UUID

from sqlalchemy.orm import Session

from app.models.foundation_design import FoundationContextRow, FoundationSelectionRow
from app.schemas.foundation_design import FoundationContext, FoundationSelectionResult


class FoundationDesignRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_context(self, context: FoundationContext) -> None:
        self._session.add(FoundationContextRow(result_id=context.result_id, context=context.model_dump(mode="json")))
        self._session.flush()

    def context(self, result_id: UUID) -> FoundationContext | None:
        row = self._session.get(FoundationContextRow, result_id)
        return None if row is None else FoundationContext.model_validate(row.context)

    def add_selection(self, result: FoundationSelectionResult) -> None:
        self._session.add(FoundationSelectionRow(
            selection_id=result.selection_id, input_hash=result.input_hash,
            selected_result_id=result.selected_result_id, outcome=result.model_dump(mode="json"),
        ))
        self._session.flush()

    def selection(self, selection_id: UUID) -> FoundationSelectionResult | None:
        row = self._session.get(FoundationSelectionRow, selection_id)
        return None if row is None else FoundationSelectionResult.model_validate(row.outcome)
