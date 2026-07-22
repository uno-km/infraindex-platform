"""Security and schema fixes

Revision ID: a1b2c3d4e5f6
Revises: dfbf6ca1c583
Create Date: 2026-07-22 20:25:00.000000

변경 내용:
  1. price_history.price_per_hour: Float → Numeric(12,6)
  2. price_history.vram_gb: Float → Numeric(8,2)
  3. price_history.sys_ram_gb: Float → Numeric(8,2)
  4. price_history.tdp_w: Float → Numeric(8,2)
  5. price_history: ix_price_history_gpu_time 복합 인덱스 추가
  6. collection_runs: FK 제거, provider_id → String(50)
  7. collection_runs: error_message Text 컬럼 추가
  8. collection_runs: ix_collection_runs_provider_started 인덱스 추가
  9. data_quality_issues: run_id FK 제거 → String(36) nullable
  10. data_quality_issues: observation_id FK 제거 → String(36) nullable
  11. data_quality_issues: raw_data_snapshot Text 컬럼 추가
  12. outbox_events: (processed, created_at) 복합 인덱스 추가
  13. idempotency_keys: executed_at 인덱스 추가 (TTL 청소용)
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "dfbf6ca1c583"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1-4. price_history: Float → Numeric ──────────────────────────────
    op.alter_column(
        "price_history", "price_per_hour",
        existing_type=sa.Float(),
        type_=sa.Numeric(precision=12, scale=6),
        existing_nullable=False,
        postgresql_using="price_per_hour::numeric(12,6)",
    )
    op.alter_column(
        "price_history", "vram_gb",
        existing_type=sa.Float(),
        type_=sa.Numeric(precision=8, scale=2),
        existing_nullable=True,
        postgresql_using="vram_gb::numeric(8,2)",
    )
    op.alter_column(
        "price_history", "sys_ram_gb",
        existing_type=sa.Float(),
        type_=sa.Numeric(precision=8, scale=2),
        existing_nullable=True,
        postgresql_using="sys_ram_gb::numeric(8,2)",
    )
    op.alter_column(
        "price_history", "tdp_w",
        existing_type=sa.Float(),
        type_=sa.Numeric(precision=8, scale=2),
        existing_nullable=True,
        postgresql_using="tdp_w::numeric(8,2)",
    )

    # ── 5. price_history: GPU + timestamp 복합 인덱스 추가 ─────────────────
    op.create_index(
        "ix_price_history_gpu_time",
        "price_history",
        ["gpu_model", "timestamp"],
        unique=False,
    )

    # ── 6-8. collection_runs 재구성 ────────────────────────────────────────
    # 기존 FK 제약 제거
    try:
        op.drop_constraint(
            "collection_runs_provider_id_fkey",
            "collection_runs",
            type_="foreignkey",
        )
    except Exception:
        # FK 이름이 다를 수 있음 (Alembic 자동 생성명 차이)
        pass

    # provider_id 타입 변경: UUID → String(50)
    op.alter_column(
        "collection_runs", "provider_id",
        existing_type=sa.Uuid(),
        type_=sa.String(length=50),
        existing_nullable=False,
        postgresql_using="provider_id::text",
    )

    # error_message 컬럼 추가
    op.add_column(
        "collection_runs",
        sa.Column("error_message", sa.Text(), nullable=True),
    )

    # 복합 인덱스 추가
    op.create_index(
        "ix_collection_runs_provider_started",
        "collection_runs",
        ["provider_id", "started_at"],
        unique=False,
    )

    # ── 9-11. data_quality_issues 재구성 ──────────────────────────────────
    # 기존 FK 제약 제거
    for fk_name in [
        "data_quality_issues_run_id_fkey",
        "data_quality_issues_observation_id_fkey",
    ]:
        try:
            op.drop_constraint(fk_name, "data_quality_issues", type_="foreignkey")
        except Exception:
            pass

    # run_id: UUID FK → String(36) nullable
    op.alter_column(
        "data_quality_issues", "run_id",
        existing_type=sa.Uuid(),
        type_=sa.String(length=36),
        nullable=True,
        postgresql_using="run_id::text",
    )

    # observation_id: UUID FK → String(36) nullable
    op.alter_column(
        "data_quality_issues", "observation_id",
        existing_type=sa.Uuid(),
        type_=sa.String(length=36),
        nullable=True,
        postgresql_using="observation_id::text",
    )

    # raw_data_snapshot 컬럼 추가
    op.add_column(
        "data_quality_issues",
        sa.Column("raw_data_snapshot", sa.Text(), nullable=True),
    )

    # ── 12. outbox_events: (processed, created_at) 복합 인덱스 ────────────
    op.create_index(
        "ix_outbox_events_pending_created",
        "outbox_events",
        ["processed", "created_at"],
        unique=False,
        postgresql_where=sa.text("processed = false"),  # 부분 인덱스 — 미처리 이벤트만
    )

    # ── 13. idempotency_keys: executed_at 인덱스 (TTL 청소용) ─────────────
    op.create_index(
        "ix_idempotency_keys_executed_at",
        "idempotency_keys",
        ["executed_at"],
        unique=False,
    )


def downgrade() -> None:
    # 인덱스 제거
    op.drop_index("ix_idempotency_keys_executed_at", table_name="idempotency_keys")
    op.drop_index("ix_outbox_events_pending_created", table_name="outbox_events")
    op.drop_index("ix_collection_runs_provider_started", table_name="collection_runs")
    op.drop_index("ix_price_history_gpu_time", table_name="price_history")

    # raw_data_snapshot 제거
    op.drop_column("data_quality_issues", "raw_data_snapshot")
    op.drop_column("collection_runs", "error_message")

    # 타입 복원 (Numeric → Float)
    op.alter_column(
        "price_history", "price_per_hour",
        existing_type=sa.Numeric(precision=12, scale=6),
        type_=sa.Float(),
        postgresql_using="price_per_hour::double precision",
    )
    op.alter_column(
        "price_history", "vram_gb",
        existing_type=sa.Numeric(precision=8, scale=2),
        type_=sa.Float(),
        postgresql_using="vram_gb::double precision",
    )
    op.alter_column(
        "price_history", "sys_ram_gb",
        existing_type=sa.Numeric(precision=8, scale=2),
        type_=sa.Float(),
        nullable=True,
        postgresql_using="sys_ram_gb::double precision",
    )
    op.alter_column(
        "price_history", "tdp_w",
        existing_type=sa.Numeric(precision=8, scale=2),
        type_=sa.Float(),
        nullable=True,
        postgresql_using="tdp_w::double precision",
    )
