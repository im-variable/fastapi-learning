"""add column middle_name in user table

Revision ID: 2af3088d3383
Revises: f452ec0d60fa
Create Date: 2024-12-23 13:25:10.332688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2af3088d3383'
down_revision: Union[str, None] = 'f452ec0d60fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('middle_name', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'middle_name')
