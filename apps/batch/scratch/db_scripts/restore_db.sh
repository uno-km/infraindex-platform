#!/bin/bash
# Restore Script for PostgreSQL Database (InfraIndex)

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore_db.sh <path_to_dump_file>"
    exit 1
fi

DUMP_FILE=$1
DB_NAME="infraindex"
DB_USER="infraindex_admin"

echo "WARNING: This will overwrite the database '$DB_NAME'."
read -p "Are you sure? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Restoring from $DUMP_FILE..."
    # Drop and recreate if necessary, or just restore
    pg_restore -U "$DB_USER" -d "$DB_NAME" -v -1 "$DUMP_FILE"
    echo "Restore completed."
else
    echo "Restore cancelled."
fi
