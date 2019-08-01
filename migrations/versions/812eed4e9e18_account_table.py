"""account table

Revision ID: 812eed4e9e18
Revises: 5ccb3836817a
Create Date: 2019-07-27 16:27:50.801624

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '812eed4e9e18'
down_revision = '5ccb3836817a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('AccountInfo',
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('account_email', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('account_status', sa.String(length=8), nullable=True),
    sa.Column('account_create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('account_id')
    )
    op.create_index(op.f('ix_AccountInfo_account_email'), 'AccountInfo', ['account_email'], unique=True)
    op.drop_table('post')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_phone_number', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('phone_number', sa.VARCHAR(length=16), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('create_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=True)
    op.create_index('ix_user_phone_number', 'user', ['phone_number'], unique=True)
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Post_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('username', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('post', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('createtime', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('record_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Post_pkey')
    )
    op.drop_index(op.f('ix_AccountInfo_account_email'), table_name='AccountInfo')
    op.drop_table('AccountInfo')
    # ### end Alembic commands ###
