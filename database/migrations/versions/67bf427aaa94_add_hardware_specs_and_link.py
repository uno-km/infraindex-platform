"""add_hardware_specs_and_link

Revision ID: 67bf427aaa94
Revises: c01af51f5bfa
Create Date: 2026-07-22 17:48:28.909983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67bf427aaa94'
down_revision: Union[str, Sequence[str], None] = 'c01af51f5bfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('price_history', sa.Column('provider_link', sa.String(length=500), nullable=True))
    op.add_column('price_history', sa.Column('sys_ram_gb', sa.Float(), nullable=True))
    op.add_column('price_history', sa.Column('tdp_w', sa.Float(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('price_history', 'tdp_w')
    op.drop_column('price_history', 'sys_ram_gb')
    op.drop_column('price_history', 'provider_link')
