"""add due_date column to todo table

Revision ID: 001_add_due_date_to_todo
Revises:
Create Date: 2026-01-24 01:40:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '001_add_due_date_to_todo'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add due_date column to todo table
    op.add_column('todo', sa.Column('due_date', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Remove due_date column from todo table
    op.drop_column('todo', 'due_date')
