"""Remove test_field

Revision ID: e8386db0c293
Revises: 17b34639f4ea
Create Date: 2024-07-30 08:10:56.867170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8386db0c293'
down_revision = '17b34639f4ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.drop_column('test_field')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test_field', sa.VARCHAR(length=50), nullable=True))

    # ### end Alembic commands ###
