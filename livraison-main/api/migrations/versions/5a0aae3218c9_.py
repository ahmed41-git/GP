"""empty message

Revision ID: 5a0aae3218c9
Revises: 
Create Date: 2021-06-22 15:47:11.888845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a0aae3218c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paiement',
    sa.Column('numTransaction', sa.Integer(), nullable=False),
    sa.Column('idLivraison', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(length=60), nullable=True),
    sa.Column('statut', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('numTransaction')
    )
    # op.drop_table('paiement')

    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('paiement')
    # ### end Alembic commands ###
