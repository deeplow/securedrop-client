"""initial migration

Revision ID: dd5e6e1d319e
Revises:
Create Date: 2018-12-06 13:57:31.297870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd5e6e1d319e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=False),
        sa.Column('journalist_designation', sa.String(length=255), nullable=False),
        sa.Column('document_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column(
            'is_flagged',
            sa.Boolean(name='is_flagged'),
            server_default='false',
            nullable=True,
        ),
        sa.Column('public_key', sa.Text(), nullable=True),
        sa.Column('fingerprint', sa.String(length=64), nullable=True),
        sa.Column('interaction_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column(
            'is_starred',
            sa.Boolean(name='is_starred'),
            server_default='false',
            nullable=True,
        ),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_sources')),
        sa.UniqueConstraint('uuid', name=op.f('uq_sources_uuid')),
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        sa.UniqueConstraint('uuid', name=op.f('uq_users_uuid')),
    )
    op.create_table(
        'replies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=True),
        sa.Column('journalist_id', sa.Integer(), nullable=True),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('is_downloaded', sa.Boolean(name='is_downloaded'), nullable=True),
        sa.ForeignKeyConstraint(
            ['journalist_id'],
            ['users.id'],
            name=op.f('fk_replies_journalist_id_users'),
        ),
        sa.ForeignKeyConstraint(
            ['source_id'],
            ['sources.id'],
            name=op.f('fk_replies_source_id_sources'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_replies')),
        sa.UniqueConstraint('uuid', name=op.f('uq_replies_uuid')),
    )
    op.create_table(
        'submissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('download_url', sa.String(length=255), nullable=False),
        sa.Column('is_downloaded', sa.Boolean(name='is_downloaded'), nullable=True),
        sa.Column('is_read', sa.Boolean(name='is_read'), nullable=True),
        sa.Column('source_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ['source_id'],
            ['sources.id'],
            name=op.f('fk_submissions_source_id_sources'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_submissions')),
        sa.UniqueConstraint('uuid', name=op.f('uq_submissions_uuid')),
    )


def downgrade():
    op.drop_table('submissions')
    op.drop_table('replies')
    op.drop_table('users')
    op.drop_table('sources')
