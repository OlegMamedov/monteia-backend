"""edit type of content

Revision ID: ef483ae5c0e8
Revises: 24bf94b66b10
Create Date: 2024-05-24 19:11:40.982106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef483ae5c0e8'
down_revision: Union[str, None] = '24bf94b66b10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('journals', 'content',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('journals', 'content',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
