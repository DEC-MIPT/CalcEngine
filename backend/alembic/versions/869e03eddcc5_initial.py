"""initial

Revision ID: 869e03eddcc5
Revises: 
Create Date: 2026-09-29 00:32:33.693052

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '869e03eddcc5'  # pragma: allowlist secret
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
