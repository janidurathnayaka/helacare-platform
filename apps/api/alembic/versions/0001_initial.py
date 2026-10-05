"""initial HelaCare schema"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "plants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(length=64), nullable=True, unique=True),
        sa.Column("sinhala_name", sa.String(length=255), nullable=True, index=True),
        sa.Column("common_name", sa.String(length=255), nullable=True, index=True),
        sa.Column("scientific_name", sa.String(length=255), nullable=True, index=True),
        sa.Column("part_used", sa.Text(), nullable=True),
        sa.Column("traditional_use", sa.Text(), nullable=False),
        sa.Column("preparation", sa.Text(), nullable=True),
        sa.Column("safety_note", sa.Text(), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("verification_status", sa.String(length=64), nullable=False, server_default="UNVERIFIED"),
        sa.Column("safety_review_status", sa.String(length=64), nullable=False, server_default="REVIEW_REQUIRED"),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "chat_audits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("language", sa.String(length=16), nullable=False),
        sa.Column("triage_level", sa.String(length=32), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("source_ids", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table("chat_audits")
    op.drop_table("plants")
