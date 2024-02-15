"""updated the user columns max length

Revision ID: 90c28485d3b1
Revises: ab4b97e31eac
Create Date: 2024-02-13 05:22:35.911128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90c28485d3b1'
down_revision: Union[str, None] = 'ab4b97e31eac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('user', 'mobile',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=15),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'mobile',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=150),
               existing_nullable=False)
    # ### end Alembic commands ###