#!/bin/bash
# Backup script for Cognio database

set -e

# Configuration
DB_PATH="${DB_PATH:-./data/memory.db}"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/memory_backup_$TIMESTAMP.db"

echo "=== Cognio Backup ==="
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Check if database exists
if [ ! -f "$DB_PATH" ]; then
    echo "Error: Database not found at $DB_PATH"
    exit 1
fi

# Backup database
echo "Backing up database..."
cp "$DB_PATH" "$BACKUP_FILE"

# Compress backup
echo "Compressing backup..."
gzip "$BACKUP_FILE"

FINAL_FILE="$BACKUP_FILE.gz"
FILE_SIZE=$(du -h "$FINAL_FILE" | cut -f1)

echo ""
echo "Backup completed successfully!"
echo "File: $FINAL_FILE"
echo "Size: $FILE_SIZE"
echo ""

# Clean up old backups (keep last 10)
echo "Cleaning old backups..."
ls -t "$BACKUP_DIR"/memory_backup_*.db.gz | tail -n +11 | xargs -r rm
echo ""

echo "Done!"
