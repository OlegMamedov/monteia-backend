"""fix problems

Revision ID: 3c6cfac8a9d5
Revises: abe4aba5eb9c
Create Date: 2024-06-19 17:29:27.308674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c6cfac8a9d5'
down_revision: Union[str, None] = 'abe4aba5eb9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('divinations', sa.Column('price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('divinations', 'price')
    # ### end Alembic commands ###
