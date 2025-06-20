"""Migración inicial con Producto y Servicio

Revision ID: 11d443ffc5a0
Revises: 
Create Date: 2025-06-16 21:58:59.030386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11d443ffc5a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=250), nullable=True),
    sa.Column('detalle', sa.String(length=250), nullable=True),
    sa.Column('precio', sa.Float(), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('servicio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=250), nullable=True),
    sa.Column('detalle', sa.String(length=250), nullable=True),
    sa.Column('precio', sa.Float(), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('servicio')
    op.drop_table('producto')
    # ### end Alembic commands ###
