"""empty message

Revision ID: de927efecec2
Revises: 
Create Date: 2017-05-17 19:39:56.761996

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'de927efecec2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repo',
                    sa.Column('id', sa.TEXT(), nullable=False),
                    sa.Column('path', sa.TEXT(), nullable=True),
                    sa.Column('deploy_path', sa.TEXT(), nullable=True),
                    sa.Column('url', sa.TEXT(), nullable=True),
                    sa.Column('last_used', sa.INTEGER(), nullable=True),
                    sa.Column('active', sa.BOOLEAN(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('deploy_path'),
                    sa.UniqueConstraint('path')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('repo')
    # ### end Alembic commands ###
