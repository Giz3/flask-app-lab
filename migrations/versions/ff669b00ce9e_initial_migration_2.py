"""Initial migration 2

Revision ID: ff669b00ce9e
Revises: 
Create Date: 2024-12-18 16:20:54.234057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'ff669b00ce9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Check if the 'tags' table already exists before creation
    bind = op.get_bind()
    inspector = inspect(bind)
    if 'tags' not in inspector.get_table_names():
        op.create_table(
            'tags',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(50), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name')
        )
    
    # Check if the 'users' table already exists before creation
    if 'users' not in inspector.get_table_names():
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(20), nullable=False),
            sa.Column('email', sa.String(120), nullable=False),
            sa.Column('password', sa.String(60), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
        )
    
    # Check if the 'post_tags' table already exists before creation
    if 'post_tags' not in inspector.get_table_names():
        op.create_table(
            'post_tags',
            sa.Column('post_id', sa.Integer(), nullable=False),
            sa.Column('tag_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['post_id'], ['posts.id']),
            sa.ForeignKeyConstraint(['tag_id'], ['tags.id']),
            sa.PrimaryKeyConstraint('post_id', 'tag_id')
        )
    
    # Alter posts table to add foreign key reference to users
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_posts_users', 'users', ['user_id'], ['id'])
        batch_op.drop_column('author')


def downgrade():
    # Reverse the changes in the downgrade function
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=20), nullable=True))
        batch_op.drop_constraint('fk_posts_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    op.drop_table('post_tags')
    op.drop_table('users')
    op.drop_table('tags')