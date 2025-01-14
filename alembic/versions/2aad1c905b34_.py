"""empty message

Revision ID: 2aad1c905b34
Revises: 6f250cc4df42
Create Date: 2025-01-14 09:57:57.595461
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2aad1c905b34'
down_revision: Union[str, None] = '6f250cc4df42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No need to add 'id' column if it's not required
    # Ensure the database schema matches your model by not making unnecessary changes
    pass  # No operations

def downgrade() -> None:
    # Drop 'id' column if it was mistakenly added
    op.drop_column('users', 'id')
