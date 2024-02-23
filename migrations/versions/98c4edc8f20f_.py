"""empty message

Revision ID: 98c4edc8f20f
Revises: 
Create Date: 2024-02-10 12:56:01.794069

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '98c4edc8f20f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('school_years')
    op.drop_table('periods')
    op.drop_table('student_assessment_scores')
    op.drop_table('assessment_standards')
    op.drop_table('users')
    op.drop_table('years')
    op.drop_table('roles')
    op.drop_table('staff')
    op.drop_table('classrooms')
    op.drop_table('classroom_schoolyear_period')
    op.drop_table('classroom_school_years')
    op.drop_table('grade_levels')
    op.drop_table('schools')
    op.drop_table('students')
    op.drop_table('assessment_details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assessment_details',
    sa.Column('id', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('short_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('family', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('subject', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('content_standard', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='assessment_details_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('student_first', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('student_last', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='students_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('schools',
    sa.Column('id', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('short_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='school_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('grade_levels',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='grade_level_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('classroom_school_years',
    sa.Column('id', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('classroom_id', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('year_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], name='classroom_school_years_classroom_id_fkey'),
    sa.ForeignKeyConstraint(['teacher_id'], ['staff.staff_id'], name='classroom_school_years_teacher_id_fkey'),
    sa.ForeignKeyConstraint(['year_id'], ['years.id'], name='classroom_school_years_year_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='classroom_school_years_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('classroom_schoolyear_period',
    sa.Column('classroomschoolyearperiodid', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('periodid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('classroomschoolyearid', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['classroomschoolyearid'], ['classroom_school_years.id'], name='fk_classroom_school_years_classroom_schoolyear_period'),
    sa.ForeignKeyConstraint(['periodid'], ['periods.id'], name='classroom_schoolyear_period_periodid_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('classroomschoolyearperiodid', name='classroom_schoolyear_period_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('classrooms',
    sa.Column('id', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('subject', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('school_id', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('grade_level_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['grade_level_id'], ['grade_levels.id'], name='classroom_gradelevelid_fkey'),
    sa.ForeignKeyConstraint(['grade_level_id'], ['grade_levels.id'], name='fk_grade_levels_classrooms'),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], name='classroom_schoolid_fkey'),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], name='fk_schools_classrooms'),
    sa.PrimaryKeyConstraint('id', name='classroom_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('staff',
    sa.Column('staff_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=319), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='fk_staff_roles'),
    sa.PrimaryKeyConstraint('staff_id', name='teacher_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('roles_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('permissions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('years',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('start_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('end_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='years_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('users',
    sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=319), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('staff_member', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('staff_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.staff_id'], name='users_staff_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', name='users_pkey')
    )
    op.create_table('assessment_standards',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('rank', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('rank_score', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True),
    sa.Column('assessment_id', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('period_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('grade_level_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['assessment_id'], ['assessment_details.id'], name='assessment_standards_assessmentid_fkey'),
    sa.ForeignKeyConstraint(['grade_level_id'], ['grade_levels.id'], name='assessment_standards_gradelevelid_fkey'),
    sa.ForeignKeyConstraint(['period_id'], ['periods.id'], name='assessment_standards_periodid_fkey'),
    sa.PrimaryKeyConstraint('id', name='assessment_standards_pkey')
    )
    op.create_table('student_assessment_scores',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('student_score', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('classroom_schoolyear_period_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('assessment_id', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['assessment_id'], ['assessment_details.id'], name='student_assessment_scores_assessment_id_fkey'),
    sa.ForeignKeyConstraint(['classroom_schoolyear_period_id'], ['classroom_schoolyear_period.classroomschoolyearperiodid'], name='student_assessment_scores_classroom_schoolyear_period_id_fkey'),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], name='student_assessment_scores_student_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='student_assessment_scores_pkey')
    )
    op.create_table('periods',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='period_pkey')
    )
    op.create_table('school_years',
    sa.Column('id', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('school_id', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('year_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('principal_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('super_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['principal_id'], ['staff.staff_id'], name='school_years_principal_id_fkey'),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], name='school_years_school_id_fkey'),
    sa.ForeignKeyConstraint(['super_id'], ['staff.staff_id'], name='school_years_super_id_fkey'),
    sa.ForeignKeyConstraint(['year_id'], ['years.id'], name='school_years_year_id_fkey')
    )
    # ### end Alembic commands ###
