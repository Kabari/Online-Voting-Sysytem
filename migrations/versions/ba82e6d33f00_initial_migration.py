"""Initial migration

Revision ID: ba82e6d33f00
Revises: 
Create Date: 2023-01-24 13:58:59.854309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba82e6d33f00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mat_no', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('batch', sa.String(length=120), nullable=False),
    sa.Column('course', sa.String(length=120), nullable=False),
    sa.Column('department', sa.String(length=120), nullable=False),
    sa.Column('post', sa.String(length=80), nullable=False),
    sa.Column('pic_path', sa.String(length=120), nullable=True),
    sa.Column('agenda', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mat_no')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mat_no', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('admin', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mat_no')
    )
    op.create_table('votes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mat_no', sa.String(), nullable=False),
    sa.Column('voter_id', sa.Integer(), nullable=True),
    sa.Column('post_1', sa.Integer(), nullable=False),
    sa.Column('post_2', sa.Integer(), nullable=False),
    sa.Column('post_3', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['voter_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mat_no')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    op.drop_table('users')
    op.drop_table('candidates')
    # ### end Alembic commands ###
