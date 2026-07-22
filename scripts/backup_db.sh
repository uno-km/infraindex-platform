#!/bin/bash
# Backup Script for PostgreSQL Database (InfraIndex)
# Run via CRON daily

set -e

BACKUP_DIR="/var/backups/infraindex"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="infraindex"
DB_USER="infraindex_admin"
# DB_PASSWORD should be in environment or .pgpass

mkdir -p "$BACKUP_DIR"

echo "Starting backup of $DB_NAME at $TIMESTAMP..."
pg_dump -U "$DB_USER" -F c -b -v -f "$BACKUP_DIR/infraindex_backup_$TIMESTAMP.dump" "$DB_NAME"
echo "Backup completed: $BACKUP_DIR/infraindex_backup_$TIMESTAMP.dump"

# Optional: Upload to S3
# aws s3 cp "$BACKUP_DIR/infraindex_backup_$TIMESTAMP.dump" s3://infraindex-backups/
