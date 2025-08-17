"""add role in user_model

Revision ID: eb9a260732f2
Revises: c2a509890463
Create Date: 2025-08-16 22:07:17.259886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb9a260732f2'
down_revision: Union[str, Sequence[str], None] = 'c2a509890463'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cria o ENUM se ainda não existir
    role_enum = sa.Enum("INTERNAL", "CLIENT", name="userrole")
    role_enum.create(op.get_bind(), checkfirst=True)

    # Adiciona a coluna usando o tipo criado
    op.add_column(
        "users",
        sa.Column("role", role_enum, nullable=False, server_default="CLIENT")
    )


def downgrade() -> None:
    # Remove a coluna
    op.drop_column("users", "role")

    # Remove o ENUM se não for mais usado
    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=True)
