"""change attribute table honeypotsensor

Revision ID: 4721bbba0040
Revises: ea7a20483456
Create Date: 2023-03-06 23:07:55.169801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4721bbba0040'
down_revision = 'ea7a20483456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('honeypot_sensor', schema=None) as batch_op:
        batch_op.alter_column('honeypot_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('sensor_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('honeypot_sensor', schema=None) as batch_op:
        batch_op.alter_column('sensor_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('honeypot_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
