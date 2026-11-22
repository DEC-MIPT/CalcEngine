from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "foundation_design_v1"
down_revision: str | Sequence[str] | None = "ae350ead9bfd"  # pragma: allowlist secret
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "foundation_context",
        sa.Column("result_id", sa.Uuid(), sa.ForeignKey("calculation_result.result_id"), primary_key=True),
        sa.Column("context", sa.JSON(), nullable=False),
    )
    op.create_table(
        "foundation_selection",
        sa.Column("selection_id", sa.Uuid(), primary_key=True),
        sa.Column("input_hash", sa.String(64), nullable=False),
        sa.Column("selected_result_id", sa.Uuid(), sa.ForeignKey("calculation_result.result_id"), nullable=True),
        sa.Column("outcome", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_foundation_selection_input_hash", "foundation_selection", ["input_hash"])


def downgrade() -> None:
    op.drop_index("ix_foundation_selection_input_hash", table_name="foundation_selection")
    op.drop_table("foundation_selection")
    op.drop_table("foundation_context")
