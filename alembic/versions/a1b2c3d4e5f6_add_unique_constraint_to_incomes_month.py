"""incomes.monthにUNIQUE制約を追加

Revision ID: a1b2c3d4e5f6
Revises: 23c8d2fee418
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '23c8d2fee418'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uq_incomes_month', 'incomes', ['month'])


def downgrade() -> None:
    op.drop_constraint('uq_incomes_month', 'incomes', type_='unique')
