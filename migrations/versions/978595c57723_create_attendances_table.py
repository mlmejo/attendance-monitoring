"""create attendances table

Revision ID: 978595c57723
Revises: c753fa56cac9
Create Date: 2024-03-03 11:15:37.123472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '978595c57723'
down_revision = 'c753fa56cac9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qrcode_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('time_in', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('time_out', sa.DateTime(), nullable=True),
    sa.Column('time_in_image', sa.Text(), nullable=True),
    sa.Column('time_out_image', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['qrcode_id'], ['qrcodes.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    # ### end Alembic commands ###