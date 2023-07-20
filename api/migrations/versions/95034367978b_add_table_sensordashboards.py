"""add table sensordashboards

Revision ID: 95034367978b
Revises: 27a1b0c29632
Create Date: 2023-05-31 15:21:32.385822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95034367978b'
down_revision = '27a1b0c29632'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensor_dashboards',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=False),
    sa.Column('dashboard_id', sa.String(), nullable=False),
    sa.Column('dashboard_url', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensor_dashboards')
    # ### end Alembic commands ###