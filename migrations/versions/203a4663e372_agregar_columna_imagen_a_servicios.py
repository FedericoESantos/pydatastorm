"""agregar columna imagen a servicios

Revision ID: 203a4663e372
Revises: 11d443ffc5a0
Create Date: 2025-06-17 21:33:24.823863

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '203a4663e372'
down_revision = '11d443ffc5a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('imagen', sa.String(length=100), nullable=True))
        batch_op.drop_column('fecha')

    with op.batch_alter_table('servicio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('imagen', sa.String(length=100), nullable=True))
        batch_op.drop_column('fecha')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('servicio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.drop_column('imagen')

    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.drop_column('imagen')

    # ### end Alembic commands ###
