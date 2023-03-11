"""add table sensors

Revision ID: 84057b391203
Revises: bf85bb5936a0
Create Date: 2023-03-06 22:09:10.369278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84057b391203'
down_revision = 'bf85bb5936a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('ip_address', sa.String(), nullable=False),
    sa.Column('state', sa.Boolean(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensors')
    # ### end Alembic commands ###
