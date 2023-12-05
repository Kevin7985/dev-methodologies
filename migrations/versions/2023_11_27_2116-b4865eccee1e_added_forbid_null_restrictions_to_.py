"""added forbid-null restrictions to bookcrossing points model

Revision ID: b4865eccee1e
Revises: 56793b73e41b
Create Date: 2023-11-27 21:16:42.683967

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'b4865eccee1e'
down_revision = '56793b73e41b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bookcrossing_points', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False,
               existing_comment='Название точки буккроссинга')
    op.alter_column('bookcrossing_points', 'latitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False,
               existing_comment='Широта')
    op.alter_column('bookcrossing_points', 'longitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False,
               existing_comment='Долгота')
    op.alter_column('bookcrossing_points', 'address_text',
               existing_type=sa.VARCHAR(),
               nullable=False,
               existing_comment='Адрес')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bookcrossing_points', 'address_text',
               existing_type=sa.VARCHAR(),
               nullable=True,
               existing_comment='Адрес')
    op.alter_column('bookcrossing_points', 'longitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True,
               existing_comment='Долгота')
    op.alter_column('bookcrossing_points', 'latitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True,
               existing_comment='Широта')
    op.alter_column('bookcrossing_points', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True,
               existing_comment='Название точки буккроссинга')
    # ### end Alembic commands ###