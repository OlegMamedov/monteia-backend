"""add table token

Revision ID: 304672f03f99
Revises: 6b1122fa6fcc
Create Date: 2024-05-21 17:54:55.066876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '304672f03f99'
down_revision: Union[str, None] = '6b1122fa6fcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
