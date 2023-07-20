"""add table honeypotsensor

Revision ID: ea7a20483456
Revises: 27a1b0c29632
Create Date: 2023-03-06 23:05:47.372814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea7a20483456'
down_revision = 'bf85bb5936a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('honeypot_sensor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('honeypot_id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['honeypot_id'], ['honeypots.id'], ),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('honeypot_sensor')
    # ### end Alembic commands ###
