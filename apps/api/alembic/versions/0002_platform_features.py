"""admin, curation, feedback, safety, analytics and vector retrieval"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = "0002_platform_features"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("plants", sa.Column("embedding", Vector(256), nullable=True))

    op.create_table(
        "source_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("plant_id", sa.Integer(), sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("institution", sa.String(255), nullable=True),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("publication_year", sa.Integer(), nullable=True),
        sa.Column("verification_status", sa.String(64), nullable=False, server_default="PENDING"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_source_records_plant_id", "source_records", ["plant_id"])
    op.create_index("ix_source_records_verification_status", "source_records", ["verification_status"])

    op.create_table(
        "practitioner_reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("plant_id", sa.Integer(), sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reviewer_name", sa.String(255), nullable=False),
        sa.Column("reviewer_role", sa.String(255), nullable=True),
        sa.Column("status", sa.String(64), nullable=False, server_default="PENDING"),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_practitioner_reviews_plant_id", "practitioner_reviews", ["plant_id"])
    op.create_index("ix_practitioner_reviews_status", "practitioner_reviews", ["status"])

    op.create_table(
        "user_feedback",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("chat_audit_id", sa.Integer(), sa.ForeignKey("chat_audits.id", ondelete="SET NULL"), nullable=True),
        sa.Column("helpful", sa.Boolean(), nullable=True),
        sa.Column("category", sa.String(64), nullable=False, server_default="GENERAL"),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("resolved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_user_feedback_chat_audit_id", "user_feedback", ["chat_audit_id"])
    op.create_index("ix_user_feedback_category", "user_feedback", ["category"])
    op.create_index("ix_user_feedback_resolved", "user_feedback", ["resolved"])

    op.create_table(
        "safety_flags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("chat_audit_id", sa.Integer(), sa.ForeignKey("chat_audits.id", ondelete="SET NULL"), nullable=True),
        sa.Column("message_excerpt", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(32), nullable=False, server_default="HIGH"),
        sa.Column("reason", sa.String(255), nullable=False, server_default="Emergency red-flag gate"),
        sa.Column("status", sa.String(64), nullable=False, server_default="OPEN"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_safety_flags_chat_audit_id", "safety_flags", ["chat_audit_id"])
    op.create_index("ix_safety_flags_severity", "safety_flags", ["severity"])
    op.create_index("ix_safety_flags_status", "safety_flags", ["status"])

    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor", sa.String(255), nullable=False, server_default="system"),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("entity_type", sa.String(64), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_audit_events_action", "audit_events", ["action"])
    op.create_index("ix_audit_events_entity_type", "audit_events", ["entity_type"])


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("safety_flags")
    op.drop_table("user_feedback")
    op.drop_table("practitioner_reviews")
    op.drop_table("source_records")
    op.drop_column("plants", "embedding")
