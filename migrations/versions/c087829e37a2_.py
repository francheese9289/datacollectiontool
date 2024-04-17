"""empty message

Revision ID: c087829e37a2
Revises: 98c4edc8f20f
Create Date: 2024-04-16 15:38:35.868286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c087829e37a2'
down_revision = '98c4edc8f20f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('Classroom','user_id')
    op.create_table('User',
                    sa.Column('user_id', sa.String, autoincrement=True, nullable=False),
                    sa.Column('user_email',sa.String),
                    sa.Column('user_first_name', sa.String),
                    sa.Column('user_last_name', sa.String),
                    sa.Column('username', sa.String),
                    sa.Column('user_password', sa.String),
                    sa.Column('user_password', sa.String),
                    sa.Column('staff_member', sa.Boolean),
                    sa.Column('staff_id', sa.String),
                    sa.ForeignKeyConstraint(['staff_id'], ['staff.staff_id'], name='users_staff_id_fkey'),
                    sa.PrimaryKeyConstraint('user_id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.add_column('Classroom',sa.Column('user_id', sa.Integer),
                  sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='classrooms_user_id_fkey'))


def downgrade():
    pass
