"""auto migration

Revision ID: a39b568b404d
Revises: 78e62267df52
Create Date: 2025-02-26 18:24:56.039142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a39b568b404d'
down_revision: Union[str, None] = '78e62267df52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.drop_column('original_name')
        batch_op.drop_column('public_url')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.add_column(sa.Column('public_url', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('original_name', sa.VARCHAR(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
