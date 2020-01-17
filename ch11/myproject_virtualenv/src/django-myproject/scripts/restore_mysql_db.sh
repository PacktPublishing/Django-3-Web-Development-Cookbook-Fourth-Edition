#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/home/myproject
REPOSITORY_PATH=${PROJECT_PATH}/src/myproject
LATEST_BACKUP_PATH=${PROJECT_PATH}/db_backups/latest.sql
export DJANGO_SETTINGS_MODULE=myproject.settings.production

cd "${PROJECT_PATH}"
source venv/bin/activate

echo "=== Restoring DB from a Backup ==="

echo "- Fill the database with schema and data"
cd "${REPOSITORY_PATH}"
zcat "${LATEST_BACKUP_PATH}.gz" | python manage.py dbshell

duration=$SECONDS
echo "------------------------------------------"
echo "The operation took $((duration / 60)) minutes and $((duration % 60)) seconds."
