"""empty message

Revision ID: 7aa7d47cece4
Revises: 2b707ec995f7
Create Date: 2024-07-22 22:27:36.631552

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7aa7d47cece4'
down_revision = '2b707ec995f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('application_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('application_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('decision_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('invoice_id', sa.Integer(), nullable=True),
    sa.Column('payment_status_code', sa.String(length=50), nullable=True),
    sa.Column('payment_completion_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('payment_account', sa.String(length=30), nullable=True),
    sa.Column('registration_id', sa.Integer(), nullable=True),
    sa.Column('submitter_id', sa.Integer(), nullable=True),
    sa.Column('reviewer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['registration_id'], ['registrations.id'], ),
    sa.ForeignKeyConstraint(['reviewer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['submitter_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_application_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_application_type'), ['type'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_application_type'))
        batch_op.drop_index(batch_op.f('ix_application_status'))

    op.drop_table('application')
    # ### end Alembic commands ###