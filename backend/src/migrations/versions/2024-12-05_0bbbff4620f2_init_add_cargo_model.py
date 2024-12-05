"""Init, add Cargo model

Revision ID: 0bbbff4620f2
Revises: 
Create Date: 2024-12-05 09:27:54.838927

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0bbbff4620f2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "cargo_rates",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type", sa.Enum("Glass", "Other", name="cargotype"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("rate", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("type", "date", name="ix_cargo_rates_type_date"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cargo_rates")
    # ### end Alembic commands ###

    op.execute("DROP TYPE cargotype")
