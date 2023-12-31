"""add post likes table

Revision ID: 56793b73e41b
Revises: 8449bd66c5ca
Create Date: 2023-11-26 17:15:13.916513

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '56793b73e41b'
down_revision = '8449bd66c5ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('post_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_likes_id'), 'likes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_likes_id'), table_name='likes')
    op.drop_table('likes')
    # ### end Alembic commands ###
