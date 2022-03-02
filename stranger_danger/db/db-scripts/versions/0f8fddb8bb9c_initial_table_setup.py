"""Initial Table Setup

Revision ID: 0f8fddb8bb9c
Revises:
Create Date: 2022-03-02 20:45:24.476539

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0f8fddb8bb9c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "classifier",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model", sa.BLOB(), nullable=True),
        sa.Column(
            "date", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "email",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("definition", sa.JSON(), nullable=True),
        sa.Column(
            "date", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "fences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("definition", sa.JSON(), nullable=True),
        sa.Column(
            "date", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("image", sa.BLOB(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column(
            "date", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("predictions")
    op.drop_table("fences")
    op.drop_table("email")
    op.drop_table("classifier")
    # ### end Alembic commands ###
