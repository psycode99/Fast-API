"""Add content column to posts table

Revision ID: 624432e4e61a
Revises: 5407ce41a3b8
Create Date: 2024-05-01 10:14:20.622727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '624432e4e61a'
down_revision: Union[str, None] = '5407ce41a3b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', "content")
    pass
