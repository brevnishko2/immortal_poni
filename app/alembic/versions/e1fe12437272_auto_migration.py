"""auto migration

Revision ID: e1fe12437272
Revises:
Create Date: 2025-02-08 22:59:54.973971

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e1fe12437272"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_phone", table_name="users")
    op.drop_index("ix_users_telegram_id", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("username", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("phone", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("telegram_id", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("is_verified", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_index("ix_users_telegram_id", "users", ["telegram_id"], unique=True)
    op.create_index("ix_users_phone", "users", ["phone"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    # ### end Alembic commands ###
