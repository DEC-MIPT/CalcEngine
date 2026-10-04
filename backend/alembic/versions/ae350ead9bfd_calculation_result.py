"""calculation_result

Revision ID: ae350ead9bfd
Revises: 869e03eddcc5
Create Date: 2026-10-02

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'ae350ead9bfd'  # pragma: allowlist secret
down_revision: str | Sequence[str] | None = '869e03eddcc5'  # pragma: allowlist secret
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add the stored calculation result (calculation-api design.md decision 4)."""
    op.create_table(
        'calculation_result',
        sa.Column('result_id', sa.Uuid(), nullable=False),
        sa.Column('calculation_type', sa.String(length=200), nullable=False),
        sa.Column('engine_version', sa.String(length=50), nullable=False),
        sa.Column('input_hash', sa.String(length=64), nullable=False),
        sa.Column('inputs', sa.JSON(), nullable=False),
        sa.Column('envelope', sa.JSON(), nullable=False),
        sa.Column('norm_sources', sa.JSON(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('result_id'),
    )
    op.create_index(
        op.f('ix_calculation_result_input_hash'), 'calculation_result', ['input_hash']
    )


def downgrade() -> None:
    """Drop the stored calculation result."""
    op.drop_index(op.f('ix_calculation_result_input_hash'), table_name='calculation_result')
    op.drop_table('calculation_result')
