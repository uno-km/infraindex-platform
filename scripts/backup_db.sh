#!/bin/bash
# ============================================================
# P2-004: PostgreSQL → S3 자동 백업 스크립트 (활성화)
# ============================================================
# 실행: ./scripts/backup_db.sh
# CRON 예시 (daily 02:30 UTC):
#   30 2 * * * /app/scripts/backup_db.sh >> /var/log/infraindex_backup.log 2>&1
#
# 필요 환경변수:
#   DATABASE_URL       PostgreSQL connection string
#   S3_BACKUP_BUCKET   S3 버킷명 (예: infraindex-backups-prod)
#   AWS_REGION         AWS 리전 (기본: ap-northeast-2)
#   PGPASSWORD         pg_dump 인증 (또는 DATABASE_URL에 포함)
#
# 의존성: pg_dump, aws-cli (v2)
# ============================================================

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/var/backups/infraindex}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
AWS_REGION="${AWS_REGION:-ap-northeast-2}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

# ── 환경변수 검증 ─────────────────────────────────────────
if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "[ERROR] DATABASE_URL is not set. Aborting backup."
  exit 1
fi

if [[ -z "${S3_BACKUP_BUCKET:-}" ]]; then
  echo "[WARN] S3_BACKUP_BUCKET not set. Backup will be local only."
  S3_UPLOAD=false
else
  S3_UPLOAD=true
fi

# ── DATABASE_URL 파싱 ──────────────────────────────────────
# 형식: postgresql[+asyncpg]://user:password@host:port/dbname
# asyncpg 접두사 제거
CLEAN_URL="${DATABASE_URL/+asyncpg/}"

# PostgreSQL 연결 정보 추출
DB_USER=$(echo "$CLEAN_URL" | sed -n 's|.*://\([^:]*\):.*|\1|p')
DB_HOST=$(echo "$CLEAN_URL" | sed -n 's|.*@\([^:/]*\).*|\1|p')
DB_PORT=$(echo "$CLEAN_URL" | sed -n 's|.*:\([0-9]*\)/.*|\1|p')
DB_NAME=$(echo "$CLEAN_URL" | sed -n 's|.*/\([^?]*\).*|\1|p')
export PGPASSWORD
PGPASSWORD=$(echo "$CLEAN_URL" | sed -n 's|.*://[^:]*:\([^@]*\)@.*|\1|p')

DB_PORT="${DB_PORT:-5432}"

if [[ -z "$DB_HOST" || -z "$DB_NAME" || -z "$DB_USER" ]]; then
  echo "[ERROR] Failed to parse DATABASE_URL. Check format: postgresql://user:pass@host:port/dbname"
  exit 1
fi

# ── 백업 디렉토리 준비 ─────────────────────────────────────
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="${BACKUP_DIR}/infraindex_backup_${TIMESTAMP}.dump"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Starting backup: ${DB_NAME}@${DB_HOST}:${DB_PORT}"

# ── pg_dump 실행 ───────────────────────────────────────────
pg_dump \
  --host="$DB_HOST" \
  --port="$DB_PORT" \
  --username="$DB_USER" \
  --format=custom \
  --blobs \
  --verbose \
  --file="$BACKUP_FILE" \
  "$DB_NAME"

BACKUP_SIZE=$(du -sh "$BACKUP_FILE" | cut -f1)
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Backup completed: ${BACKUP_FILE} (${BACKUP_SIZE})"

# ── S3 업로드 ──────────────────────────────────────────────
if [[ "$S3_UPLOAD" == "true" ]]; then
  S3_KEY="backups/postgres/${DB_NAME}/${TIMESTAMP}/infraindex_backup_${TIMESTAMP}.dump"
  S3_URI="s3://${S3_BACKUP_BUCKET}/${S3_KEY}"

  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Uploading to ${S3_URI} ..."
  aws s3 cp "$BACKUP_FILE" "$S3_URI" \
    --region "$AWS_REGION" \
    --storage-class STANDARD_IA \
    --sse AES256 \
    --metadata "db=${DB_NAME},host=${DB_HOST},timestamp=${TIMESTAMP}"

  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] S3 upload successful: ${S3_URI}"

  # ── 로컬 파일 정리 (S3 업로드 성공 후 7일 이상 로컬 파일 삭제) ──
  find "$BACKUP_DIR" -name "*.dump" -mtime +7 -delete
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Local backups older than 7 days cleaned."

  # ── S3 오래된 백업 정리 (Lifecycle Policy 권장, 여기선 CLI로 보조) ──
  CUTOFF_DATE=$(date -u -d "${RETENTION_DAYS} days ago" +%Y-%m-%d 2>/dev/null || \
                date -u -v-${RETENTION_DAYS}d +%Y-%m-%d)
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] S3 retention: keeping last ${RETENTION_DAYS} days (cutoff: ${CUTOFF_DATE})"
else
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] S3_BACKUP_BUCKET not set — local backup only: ${BACKUP_FILE}"
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Backup job done."
exit 0
