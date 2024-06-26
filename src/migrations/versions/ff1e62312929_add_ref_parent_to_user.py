"""add ref_parent to user

Revision ID: ff1e62312929
Revises: 571cc70b428f
Create Date: 2024-06-24 15:56:39.264561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff1e62312929'
down_revision: Union[str, None] = '571cc70b428f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('referal_parent', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'referal_parent')
    # ### end Alembic commands ###
