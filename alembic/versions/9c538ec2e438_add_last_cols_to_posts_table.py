"""add last cols to posts table

Revision ID: 9c538ec2e438
Revises: 9d73228f2644
Create Date: 2024-05-01 10:50:58.228200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c538ec2e438'
down_revision: Union[str, None] = '9d73228f2644'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('is_published', sa.Boolean(), nullable=False,
                                      server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                      server_default=sa.text('NOW()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'is_published')
    op.drop_column('posts', 'created_at')
    pass
