"""добавлен атрибут genre в сущность книги

Revision ID: c20f5e595f73
Revises: 694cee0d5cd3
Create Date: 2023-10-07 23:40:02.058654

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c20f5e595f73'
down_revision = '694cee0d5cd3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('genre', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Жанры'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'genre')
    # ### end Alembic commands ###
