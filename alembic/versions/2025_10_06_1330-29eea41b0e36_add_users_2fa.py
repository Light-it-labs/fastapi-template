"""add users_2fa

Revision ID: 29eea41b0e36
Revises: 77b76554607d
Create Date: 2025-10-06 13:30:29.944265

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "29eea41b0e36"
down_revision: Union[str, None] = "77b76554607d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users_2fa",
        sa.Column("secret_key", sa.String(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_users_2fa_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users_2fa")),
    )


def downgrade() -> None:
    op.drop_table("users_2fa")
