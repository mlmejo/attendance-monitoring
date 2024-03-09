"""change column types in faculty_loads

Revision ID: 649b12751e34
Revises: da0af5f9040a
Create Date: 2024-03-01 09:47:11.230213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '649b12751e34'
down_revision = 'da0af5f9040a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('faculty_loads', schema=None) as batch_op:
        batch_op.alter_column('time_start',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Time(),
               existing_nullable=False)
        batch_op.alter_column('time_end',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Time(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('faculty_loads', schema=None) as batch_op:
        batch_op.alter_column('time_end',
               existing_type=sa.Time(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('time_start',
               existing_type=sa.Time(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###
