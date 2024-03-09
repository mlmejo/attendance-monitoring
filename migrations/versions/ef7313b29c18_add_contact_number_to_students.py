"""add contact_number to students

Revision ID: ef7313b29c18
Revises: a106fcf1fc3d
Create Date: 2024-03-09 04:21:42.889989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef7313b29c18'
down_revision = 'a106fcf1fc3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact_number', sa.String(length=64), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.drop_column('contact_number')

    # ### end Alembic commands ###