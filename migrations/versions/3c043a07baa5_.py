"""empty message

Revision ID: 3c043a07baa5
Revises: 917ec1b1a57b
Create Date: 2024-04-24 16:14:02.712637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c043a07baa5'
down_revision = '917ec1b1a57b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment_score', schema=None) as batch_op:
        batch_op.alter_column('classroom_id',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('student_classroom_association', schema=None) as batch_op:
        batch_op.alter_column('classroom_id',
               existing_type=sa.VARCHAR(),
               nullable=False)


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student_classroom_association', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.alter_column('classroom_id',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('assessment_score', schema=None) as batch_op:
        batch_op.alter_column('classroom_id',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###
