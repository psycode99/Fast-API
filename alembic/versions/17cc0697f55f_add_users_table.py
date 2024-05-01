"""add users table

Revision ID: 17cc0697f55f
Revises: 624432e4e61a
Create Date: 2024-05-01 10:28:15.650674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17cc0697f55f'
down_revision: Union[str, None] = '624432e4e61a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                               server_default=sa.text('now()'), nullable=False),
                               sa.PrimaryKeyConstraint('id'),
                               sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
